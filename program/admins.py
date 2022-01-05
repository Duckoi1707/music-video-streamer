from cache.admins import admins
from driver.veez import call_py
from pyrogram import Client, filters
from driver.decorators import authorized_users_only
from driver.filters import command, other_filters
from driver.queues import QUEUE, clear_queue
from driver.utils import skip_current_song, skip_item
from config import BOT_USERNAME, GROUP_SUPPORT, IMG_3, UPDATES_CHANNEL
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 Quay lại", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🗑 Close", callback_data="cls")]]
)


@Client.on_message(command(["tailaibot", f"tailaibot@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ Bot **tải lại một cách chính xác !**\n✅ ** Danh sách quản trị viên ** đã ** cập nhật !**"
    )


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "boqua"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="• Mᴇɴᴜ", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="• Cʟᴏsᴇ", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ không có gì hiện đang chơi")
        elif op == 1:
            await m.reply("✅ __Hàng đợi__ ** trống.**\n\n**• userbot rời khỏi cuộc trò chuyện thoại**")
        elif op == 2:
            await m.reply("🗑️ **Xóa hàng đợi**\n\n**• userbot rời khỏi cuộc trò chuyện thoại**")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"⏭ **Đã bỏ qua bài hát tiếp theo.**\n\n🏷 **Tên:** [{op[0]}]({op[1]})\n💡 **Trạng thái:** `Playing`\n🎧 **Yêu cầu bởi:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **removed song from queue:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["stop", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "tat"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ Người dùng đã ngắt kết nối khỏi cuộc trò chuyện video.")
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **không có gì đang phát trực tuyến**")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "tamdung"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "⏸ **Theo dõi bị tạm dừng.**\n\n• ** Để tiếp tục luồng, hãy sử dụng**\n» /tiếp tục lệnh."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **nothing in streaming**")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "tieptuc"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▶️ **Đã tiếp tục theo dõi.**\n\n• **Để tạm dừng luồng, hãy sử dụng**\n» /lệnh tạm dừng."
            )
        except Exception as e:
            await m.reply(f"🚫 **lỗi:**\n\n`{e}`")
    else:
        await m.reply("❌ **không có gì trong phát trực tuyến**")


@Client.on_message(
    command(["mmute", f"mmute@{BOT_USERNAME}", "vcmute"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 **Userbot bị tắt tiếng.**\n\n• **Để bật tiếng người dùng, hãy sử dụng**\n» /bật tiếng lệnh."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **không có gì trong phát trực tuyến**")


@Client.on_message(
    command(["munmute", f"munmute@{BOT_USERNAME}", "vcunmute"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 **Người dùng đã bật tiếng.**\n\n• **Để tắt tiếng userbot, hãy sử dụng**\n» /lệnh tắt tiếng."
            )
        except Exception as e:
            await m.reply(f"🚫 **lỗi:**\n\n`{e}`")
    else:
        await m.reply("❌ **không có gì trong phát trực tuyến**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("bạn là Quản trị viên Ẩn danh! \n \n »hoàn nguyên về tài khoản người dùng từ quyền quản trị viên.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 chỉ quản trị viên có quyền quản lý cuộc trò chuyện thoại mới có thể nhấn vào nút này !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "⏸ phát trực tuyến đã tạm dừng", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ hiện không có gì đang phát trực tuyến", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("bạn là Quản trị viên Ẩn danh! \n \n »hoàn nguyên về tài khoản người dùng từ quyền quản trị viên.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 chỉ quản trị viên có quyền quản lý cuộc trò chuyện thoại mới có thể nhấn vào nút này !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "▶️ phát trực tuyến đã tiếp tục", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌hiện không có gì đang phát trực tuyến", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("bạn là Quản trị viên Ẩn danh! \n \n »hoàn nguyên về tài khoản người dùng từ quyền quản trị viên.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 chỉ quản trị viên có quyền quản lý cuộc trò chuyện thoại mới có thể nhấn vào nút này !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **luồng này đã kết thúc**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ hiện không có gì đang phát trực tuyến", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("bạn là Quản trị viên Ẩn danh! \n \n »hoàn nguyên về tài khoản người dùng từ quyền quản trị viên.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 chỉ quản trị viên có quyền quản lý cuộc trò chuyện thoại mới có thể nhấn vào nút này !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 userbot bị tắt tiếng thành công", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ hiện không có gì đang phát trực tuyến", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("bạn là Quản trị viên Ẩn danh! \n \n »hoàn nguyên về tài khoản người dùng từ quyền quản trị viên.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 chỉ quản trị viên có quyền quản lý cuộc trò chuyện thoại mới có thể nhấn vào nút này !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 userbot được bật tiếng thành công", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ hiện không có gì đang phát trực tuyến", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "amthanh"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"✅ **âm lượng được đặt thành** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **không có gì trong phát trực tuyến**")
