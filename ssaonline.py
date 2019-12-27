import discord
from discord.utils import get
import csv
from ftplib import FTP
from io import StringIO
import io
import json
from lxml import html
import requests


client = discord.Client()

@client.event
async def on_member_update(before, after):
    ssa = client.get_guild(644020702680186891)
    role_list_clear = [
        get(ssa.roles, name="Siege TTS"),
        get(ssa.roles, name="Siege TTS - Ranked"),
        get(ssa.roles, name="Siege Live"),
        get(ssa.roles, name="Siege Live - Ranked")
    ]

    if before.activity != after.activity:
        await after.remove_roles(*role_list_clear)

        if "356876590342340608" in str(after.activity):
            if "ranked" in str(after.activity):
                await after.add_roles(get(ssa.roles, name="Siege TTS - Ranked"))
            else:
                await after.add_roles(get(ssa.roles, name="Siege TTS"))

        elif "445956193924546560" in str(after.activity):
            if "ranked" in str(after.activity):
                await after.add_roles(get(ssa.roles, name="Siege Live - Ranked"))
            else:
                await after.add_roles(get(ssa.roles, name="Siege Live"))

        else:
            await after.remove_roles(*role_list_clear)

@client.event
async def on_message(message):
    channel = client.get_channel(649432520911224843)
    msg1 = await channel.fetch_message(651931625894051842)
    msg2 = await channel.fetch_message(651931628238667806)
    if message.channel.id == 649432520911224843:
        if message.content.startswith("$reg "):
            if message.content.count(" ") == 1:
                ftp = FTP('ftp.raycroza.com') 
                ftp.login('raycroza',"idon'tbelonghere98@raycroza")
                r = StringIO()
                ftp.retrlines('RETR /storage/discord-bot/SiegeSA/reg-user.json', r.write)
                reg_user = json.loads(r.getvalue())
                if not str(message.author.id) in r.getvalue():
                    reg_user.append({"discord_username":message.author.name,"uplay_id":message.content.replace("$reg ",""),"discord_id":str(message.author.id)})
                    user_dump = bytes(json.dumps(reg_user), 'utf-8')
                    bio = io.BytesIO(user_dump)
                    ftp.storbinary('STOR /storage/discord-bot/SiegeSA/reg-user.json', bio)
                    
                    sorted_users = []
                    for user in reg_user:
                        sorted_users.append(f'{user["discord_username"]} | {user["uplay_id"]}')
                    user_list = ', '.join(sorted(sorted_users)).replace(", ","\n").replace("_","\_") 

                    await msg1.edit(content=f'Registered Users:\n\n{user_list}\n ---')
                    await msg2.edit(content=f'{len(reg_user)}/{len(client.users)} registered.')
                    await message.delete()
                else:
                    await message.delete()
            else:
                await message.delete()

        elif message.content.startswith("$change "):
            if message.content.count(" ") == 1:
                ftp = FTP('ftp.raycroza.com') 
                ftp.login('raycroza',"idon'tbelonghere98@raycroza")
                r = StringIO()
                ftp.retrlines('RETR /storage/discord-bot/SiegeSA/reg-user.json', r.write)
                reg_user = json.loads(r.getvalue())
                if str(message.author.id) in r.getvalue():
                    for user in reg_user:
                        if user['discord_id'] == str(message.author.id):
                            user['uplay_id'] = message.content.replace("$change ","")

                    user_dump = bytes(json.dumps(reg_user), 'utf-8')
                    bio = io.BytesIO(user_dump)
                    ftp.storbinary('STOR /storage/discord-bot/SiegeSA/reg-user.json', bio)
                    
                    sorted_users = []
                    for user in reg_user:
                        sorted_users.append(f'{user["discord_username"]} | {user["uplay_id"]}')
                    user_list = ', '.join(sorted(sorted_users)).replace(", ","\n").replace("_","\_") 

                    await msg1.edit(content=f'Registered Users:\n\n{user_list}\n ---')
                    await msg2.edit(content=f'{len(reg_user)}/{len(client.users)} registered.')
                    await message.delete()
                else:
                    await message.delete()
            else:
                await message.delete()
        else:
            await message.delete()
        

client.run('NjQ0MjA4NTE5ODQ3MDg0MDQz.XcwsEg.z9e2lWaUpoOnGmyC3yNj5kkB8lQ')