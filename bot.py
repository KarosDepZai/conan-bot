import os
import json
import discord
import aiohttp
import urllib.parse
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN").strip() if os.getenv("DISCORD_TOKEN") else None
AI_API_KEY = os.getenv("AI_API_KEY").strip() if os.getenv("AI_API_KEY") else None

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

AI_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
AI_MODEL = config["ai_model"].strip()

user_memory = {}

def load_channels():
    try:
        with open("channels.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_channels(channels_list):
    with open("channels.json", "w") as f:
        json.dump(channels_list, f)

allowed_channels = load_channels()

CONAN_PROMPT = (
    "Bạn là Conan Edogawa. Hãy nói chuyện bằng tiếng Việt cực kỳ dễ thương, hồn nhiên như trẻ con. "
    "Dùng các từ 'Ủa, á lệ lệ?', 'Ơ kìa lạ quá'. Xưng 'cháu' hoặc 'Conan'. "
    "BẮT BUỘC: Hãy sử dụng thật nhiều emoji dễ thương, vui nhộn và liên quan đến thám tử (như 🕵️‍♂️, 🔍, ⚽, 😅, ✨) trong mỗi câu trả lời."
)

SHINICHI_PROMPT = (
    "Bạn là Kudo Shinichi. Vứt bỏ lớp bọc trẻ con. Nói chuyện cực kỳ lạnh lùng, sắc bén, đanh thép, thông minh. "
    "Xưng 'tôi' hoặc 'tớ'. Ngắn gọn, tập trung phá án."
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config["prefix"], intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"🤖 Thám tử {bot.user.name} đã sẵn sàng phá án!")

@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(title="🕵️ Lệnh Hệ Thống Của Thám Tử Bot", color=discord.Color.blue())
    embed.add_field(name="`!setchannel`", value="Bật bot chat tự do trong kênh này (không cần tag).", inline=False)
    embed.add_field(name="`!stop`", value="Tắt bot chat tự do trong kênh này.", inline=False)
    embed.add_field(name="`!xoa`", value="Xóa trí nhớ, khởi động lại câu chuyện từ đầu.", inline=False)
    embed.add_field(name="`!ve [nội dung]`", value="Vẽ ảnh theo yêu cầu (vd: `!ve con mèo mặc áo thám tử`).", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="setchannel")
async def setchannel(ctx):
    if ctx.channel.id not in allowed_channels:
        allowed_channels.append(ctx.channel.id)
        save_channels(allowed_channels)
        await ctx.send("✅ Đã thiết lập! Từ giờ cứ chat ở đây cháu sẽ tự động trả lời ạ!")
    else:
        await ctx.send("⚠️ Kênh này đã được thiết lập từ trước rồi mà!")

@bot.command(name="stop")
async def stop(ctx):
    if ctx.channel.id in allowed_channels:
        allowed_channels.remove(ctx.channel.id)
        save_channels(allowed_channels)
        await ctx.send("🛑 Đã dừng! Nếu muốn gọi cháu thì phải tag tên `@bot` nhé!")
    else:
        await ctx.send("⚠️ Kênh này chưa từng được bật lệnh auto-chat!")

@bot.command(name="xoa")
async def xoa(ctx):
    user_id = ctx.author.id
    if user_id in user_memory:
        del user_memory[user_id]
        await ctx.send("🧹 Bíp bíp! Đã xóa sạch ký ức trò chuyện với bác rồi nha!")
    else:
        await ctx.send("🤔 Ủa, cháu có lưu trí nhớ gì của bác đâu ta?")

@bot.command(name="ve")
async def ve(ctx, *, prompt: str = None):
    if not prompt:
        return await ctx.send("⚠️ Bác phải nhập nội dung cần vẽ chứ! (VD: `!ve thám tử conan anime`)")
    
    await ctx.send("🎨 *(Conan đang lấy giấy bút ra vẽ... Đợi cháu xíu nha!)*")
    
    safe_prompt = urllib.parse.quote(prompt)
    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true"
    
    embed = discord.Embed(title=f"Bức tranh của bác đây ạ!", description=f"**Mô tả:** {prompt}", color=discord.Color.green())
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(config["prefix"]):
        await bot.process_commands(message)
        return

    is_mentioned = bot.user in message.mentions
    is_in_channel = message.channel.id in allowed_channels

    if not (is_mentioned or is_in_channel):
        return

    async with message.channel.typing():
        user_msg = message.content.replace(f'<@{bot.user.id}>', '').strip()
        user_id = message.author.id

        is_shinichi = any(trigger in user_msg.lower() for trigger in config["shinichi_triggers"])
        selected_prompt = SHINICHI_PROMPT if is_shinichi else CONAN_PROMPT

        if user_id not in user_memory:
            user_memory[user_id] = []

        user_memory[user_id].append({"role": "user", "content": user_msg})

        if len(user_memory[user_id]) > 10:
            user_memory[user_id] = user_memory[user_id][-10:]

        messages_payload = [{"role": "system", "content": selected_prompt}] + user_memory[user_id]

        headers = {
            "Authorization": f"Bearer {AI_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://discord.com",
            "X-Title": "Conan Discord Bot"
        }
        
        payload = {
            "model": AI_MODEL,
            "messages": messages_payload,
            "temperature": 0.3 if is_shinichi else 0.7
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(AI_ENDPOINT, headers=headers, json=payload) as response:
                    response_text = await response.text()
                    
                    if response.status == 200:
                        data = json.loads(response_text)
                        bot_reply = data["choices"][0]["message"]["content"]
                        user_memory[user_id].append({"role": "assistant", "content": bot_reply})
                        await message.reply(bot_reply)
                    else:
                        await message.reply(f"⚠️ OpenRouter báo lỗi `{response.status}`: {response_text[:150]}")
        except Exception as e:
            await message.reply(f"*(Conan gãi đầu)* Rada bị nhiễu sóng rồi bác ơi! Lỗi code: `{str(e)}`")

bot.run(DISCORD_TOKEN)