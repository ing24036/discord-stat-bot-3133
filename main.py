
import discord
from discord.ext import commands
import pandas as pd
import os
from keep_alive import keep_alive  # 👈 สำคัญ

# โหลดข้อมูล Excel
def load_data():
    return pd.read_excel("dataTestDiscord.xlsx")

# ตั้งค่า intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# แสดงสถานะเมื่อบอทออนไลน์
@bot.event
async def on_ready():
    print(f"✅ Bot is ready. Logged in as {bot.user}")

# คำสั่ง !stat <governor_id>
@bot.command(name="stat")
async def stat(ctx, governor_id: int):
    df = load_data()
    user_data = df[df['Governor ID'] == governor_id]

    if user_data.empty:
        await ctx.send("❌ ไม่พบข้อมูล Governor ID นี้")
    else:
        row = user_data.iloc[0]

        embed = discord.Embed(
            title=f"📊 สถิติของ {row['exactName']}",
            description=f"🆔 Governor ID: `{row['Governor ID']}`",
            color=0x00BFFF
        )

        embed.add_field(name="🏆 Score", value=f"{row['Score']:,}", inline=True)
        embed.add_field(name="🎯 Goal", value=f"{row['Score Goal']:,}", inline=True)
        embed.add_field(name="📈 Rate", value=f"{row['rate %']:.2f}%", inline=True)
        embed.add_field(name="⚡ Starting Power", value=f"{row['starting-power']:,}", inline=True)
        embed.add_field(name="🔻 Power Change", value=f"{row['Power-change']:,}", inline=True)
        embed.add_field(name="🛡️ T4 Kills", value=f"{row['T4-Kills-gained']:,}", inline=True)
        embed.add_field(name="⚔️ T5 Kills", value=f"{row['T5-Kills-gained']:,}", inline=True)
        embed.add_field(name="💀 Dead Troops", value=f"{row['Dead Troops-gained']:,}", inline=True)
        embed.add_field(name="📦 Kill Point gained", value=f"{row['KP-gained(T4 + T5)']:,}", inline=True)

        embed.set_footer(text="พัฒนาโดย Ing")
        await ctx.send(embed=embed)

# ✅ เพิ่ม error handler เมื่อไม่ใส่ ID
@stat.error
async def stat_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ กรุณาใส่ Governor ID ด้วย เช่น `!stat 12345678`")

# ✅ เปิดเว็บ keep_alive server
keep_alive()

# ✅ รันบอทด้วย Token จาก ENV (แนะนำ)

bot.run(os.environ["DISCORD_BOT_TOKEN"])




