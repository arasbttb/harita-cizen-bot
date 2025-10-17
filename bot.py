from config import *
from logic import *
import discord
from discord.ext import commands
from config import TOKEN

# Veri tabanı yöneticisini başlatma
manager = DB_Map("database.db")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot başlatıldı!")

@bot.command()
async def start(ctx: commands.Context):
    await ctx.send(f"Merhaba, {ctx.author.name}. Mevcut komutların listesini keşfetmek için !help_me yazın.")

@bot.command()
async def help_me(ctx: commands.Context):
    await ctx.send("`!start` - bot ile çalışmaya başlayın ve bir hoş geldin mesajı alın.\n"
        "`!help_me` - mevcut komutların listesini alın\n"
        "`!show_city <şehir_adı>` - belirtilen şehri haritada gösterin.\n"
        "`!remember_city <şehir_adı>` - belirtilen şehri kaydedin.\n"
        "`!show_my_cities` - kaydettiğiniz tüm şehirleri gösterin."
        # Kullanılabilir komutların listesini gösterecek olan komutu yazın.
    )

@bot.command()
async def show_city(ctx: commands.Context, *, city_name=""):
    coordinates = manager.get_coordinates(city_name)
    if coordinates:
        await ctx.send(f'{city_name} şehrinin koordinatları: Enlem {coordinates[0]}, Boylam {coordinates[1]}')

        image_path = "show_city_map.png"
        manager.create_graph(image_path, [city_name])  # Tek şehir için liste olarak veriyoruz

        file = discord.File(image_path, filename="show_city_map.png")
        await ctx.send("İşte harita üzerinde şehir konumunuz:", file=file)
    else:
        await ctx.send("Şehir bulunamadı. Lütfen şehir adını İngilizce olarak ve komuttan sonra bir boşluk bırakarak girin.")


   

@bot.command()
async def show_my_cities(ctx: commands.Context):
    cities = manager.select_cities(ctx.author.id)  # Kullanıcının kaydettiği şehirlerin listesini alma

    if not cities:
        await ctx.send("Henüz hiç şehir kaydetmediniz. !remember_city <şehir_adı> komutuyla şehir ekleyebilirsiniz.")
        return

    await ctx.send(f'Sizin şehirleriniz: {", ".join(cities)}')

    # Haritayı oluştur ve kaydet
    image_path = "my_cities_map.png"
    manager.create_graph(image_path, cities)

    # Discord'a görseli gönder
    file = discord.File(image_path, filename="my_cities_map.png")
    await ctx.send("İşte şehirlerinizin harita üzerindeki konumu:", file=file)


   

@bot.command()
async def remember_city(ctx: commands.Context, *, city_name=""):
    if manager.add_city(ctx.author.id, city_name):  # Şehir adının format uygunluğunu kontrol etme. Başarılıysa şehri kaydet!
        await ctx.send(f'{city_name} şehri başarıyla kaydedildi!')
    else:
        await ctx.send("Hatalı format. Lütfen şehir adını İngilizce olarak ve komuttan sonra bir boşluk bırakarak girin.")

if __name__ == "__main__":
    bot.run(TOKEN)
