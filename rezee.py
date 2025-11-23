# Kontol
import asyncio
import random
import os
import sys
from telethon import TelegramClient, events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.account import UpdateProfileRequest

SESSION = os.getenv("SESSION") 
OWNER_ID = os.getenv("OWNER_ID") 
LOG_CHANNEL = os.getenv("LOG_CHANNEL") 
api_id = 2040
api_hash = "b18441a1ff607e10a989891a5462e627"

prefix = '.'
developer_username = '@cloneganteng1'
bot_name = 'Rezee Userbot'
blacklisted_groups = []

print("Starting Rezee Ubot...")
client = TelegramClient(StringSession(SESSION), api_id, api_hash)


async def get_username(user_id):
    try:
        user = await client.get_entity(user_id)
        return user.username if user.username else "No Username"
    except:
        return "Unknown"

async def get_group_name(group_id):
    try:
        group = await client.get_entity(group_id)
        return group.title if hasattr(group, 'title') else "Unknown Group"
    except:
        return "Unknown Group"

@client.on(events.NewMessage(pattern=rf'^{prefix}menu$'))
async def menu_handler(event):
    sender = await event.get_sender()
    username = sender.username if sender.username else "User"
    
    menu_text = f"""
( 👋 ) Hi {username} Welcome To Rezee Userbot Menu

╭═━≫ 𝗜 𝗡 𝗙 𝗢 𝗥 𝗠 𝗔 𝗧 𝗜 𝗢 𝗡
┃▢ ᴅᴇᴠᴇʟᴏᴘᴇʀ  : {developer_username}
┃▢ ʙᴏᴛ ɴᴀᴍᴇ : {bot_name}
┃▢ ᴠᴇʀsɪᴏɴ : 1.0
╰═━═━═━═━═━═━═━≫
╭═━═━═━⪩「 M E N U 」
┃—▢ .cfd
┃—▢ .addbl
┃—▢ .unbl
┃—▢ .spam
┃—▢ .clone
╰═━═━═━═━═━═━═━≫
    """
    await event.reply(menu_text)

@client.on(events.NewMessage(pattern=rf'^{prefix}cfd$'))
async def broadcast_handler(event):
    if not event.is_reply:
        await event.reply("Harus reply pesan yang mau di broadcast!")
        return
    
    try:

        replied_msg = await event.get_reply_message()
        
       
        dialogs = await client.get_dialogs()
        groups = [dialog for dialog in dialogs if dialog.is_group]
        
        success = 0
        failed = 0
        
        await event.reply(f"Memulai broadcast ke {len(groups)} grup...")
        
        for group in groups:
            try:
                if group.id not in blacklisted_groups:
                    await client.send_message(group.entity, replied_msg)
                    success += 1
                    await asyncio.sleep(1)  
            except Exception as e:
                failed += 1
                continue
        
        await event.reply(f"Broadcast Selesai!\n\nSukses: `{success}`\nGagal: `{failed}`")
        
    except Exception as e:
        await event.reply(f"Error: {str(e)}")

@client.on(events.NewMessage(pattern=rf'^{prefix}addbl$'))
async def add_blacklist_handler(event):
    if not event.is_group:
        await event.reply("Command ini hanya bisa digunakan di grup!")
        return
    
    try:
        chat_id = event.chat_id
        if chat_id not in blacklisted_groups:
            blacklisted_groups.append(chat_id)
            group_name = await get_group_name(chat_id)
            await event.reply(f"Sukses menambahkan grup {group_name} ke list jembut [ {bot_name} ]")
        else:
            await event.reply("Grup ini sudah ada di blacklist!")
    except Exception as e:
        await event.reply(f"Error: {str(e)}")

@client.on(events.NewMessage(pattern=rf'^{prefix}unbl$'))
async def remove_blacklist_handler(event):
    if not event.is_group:
        await event.reply("Command ini hanya bisa digunakan di grup!")
        return
    
    try:
        chat_id = event.chat_id
        if chat_id in blacklisted_groups:
            blacklisted_groups.remove(chat_id)
            group_name = await get_group_name(chat_id)
            await event.reply(f"Sukses menghapus grup {group_name} dari blacklist")
        else:
            await event.reply("Grup ini tidak ada di blacklist!")
    except Exception as e:
        await event.reply(f"Error: {str(e)}")

@client.on(events.NewMessage(pattern=rf'^{prefix}spam(?:\s+(\d+))?$'))
async def spam_handler(event):
    try:
        args = event.pattern_match.group(1)
        if not event.is_reply or not args:
            await event.reply("Format: `.spam <jumlah>` (reply pesan)")
            return
        
        count = int(args)
        if count > 1200:
            await event.reply("Maksimal 1200 spam!")
            return
        
        replied_msg = await event.get_reply_message()
        text = replied_msg.text
        
        await event.reply(f"Memulai spam {count} pesan...")
        
        for i in range(count):
            await client.send_message(event.chat_id, text)
            await asyncio.sleep(0.4)   
        
        await event.reply(f"Spam {count} pesan selesai!")
        
    except Exception as e:
        await event.reply(f"Error: {str(e)}")

@client.on(events.NewMessage(pattern=rf'^{prefix}clone(?:\s+(@?\w+))?$'))
async def clone_handler(event):
    try:
        username = event.pattern_match.group(1)
        if not username:
            await event.reply("Format: `.clone @username`")
            return
        
        username = username.replace('@', '')
        
        await event.reply(f"🔍 Mencari user @{username}...")
        
        user = await client.get_entity(username)
        
        await client(UpdateProfileRequest(
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            about=user.about or ""
        ))
        
     
        if user.photo:
            photo = await client.download_profile_photo(user, file=bytes)
            await client(UploadProfilePhotoRequest(await client.upload_file(photo)))
        
        await event.reply(f"Berhasil clone @{username}!")
        
    except Exception as e:
        await event.reply(f"Error: {str(e)}")



async def main():
    await client.start()
    print("Rezee Ubot berhasil dijalankan!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
