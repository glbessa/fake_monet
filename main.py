import discord
import os
import io
from PIL import Image
from dotenv import load_dotenv
from cycle_gan import load_generator, generate_stylized_image

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
model = None

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    elif message.content.startswith('!style'):
        try:
            buffer = await message.attachments[0].read()
            image = Image.open(io.BytesIO(buffer))
            
            stylized_image: Image = generate_stylized_image(model, image)

            buffer = io.BytesIO()
            stylized_image.save(buffer, format='PNG')
            buffer.seek(0) 
            await message.channel.send(file=discord.File(buffer, 'stylized_image.png'))
        except Exception as e:
            await message.channel.send('Error processing image')

if __name__ == '__main__':
    load_dotenv()
    model = load_generator(os.getenv('MODEL_PATH'))
    bot.run(os.getenv('DISCORD_TOKEN'))