import os
import time
import TelegramApi
import Buttons
import FilesystemMySQL

RED_PIC = "https://raw.githubusercontent.com/Jochnickel/telegram_bot_cloud/main/delete.png"
BG_PIC = "https://cdn.pixabay.com/photo/2020/07/19/13/18/sky-5420026__340.jpg"
EMPTY_SKY = "https://cdn.pixabay.com/photo/2020/07/19/13/18/sky-5420026__340.jpg"
DONATE = "Paypal: joachim.redmi@gmail.com"
BOTS_ARCHIVE_LINK = "https://t.me/BotsArchive/1559"
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

msgAdmin = None  # To be injected
errorAdmin = None  #

api = TelegramApi.TelegramApi(TOKEN)
fs = FilesystemMySQL.FilesystemMySQL()

def sendMessage(tgUserId, text, buttonArrayArray=None):
    #because wtf python. static variable?
    buttonArrayArray = buttonArrayArray or [[]]
    buttonArrayArray.append([Buttons.getDeleteMessageButton()])
    api.sendMessage(tgUserId, text, buttonArrayArray)

def sendPhoto(updateMsg, tgUserId, photo, caption, button_array_array):
    if updateMsg:
        info = api.editMessageMedia(
            chat_id=tgUserId,
            mediaType='photo',
            media=photo,
            message_id=updateMsg,
            button_array_array=button_array_array,
            caption=caption)
        
        if info[0] or info[1].count('are exactly the same'):
            return info
        # editMedia on voice message
        
    info = api.sendPhoto(
        chat_id=tgUserId,
        photo=photo,
        caption=caption,
        button_array_array=button_array_array)
        
    if info[0] and updateMsg:
        api.deleteMessage(tgUserId,updateMsg)
        
    return info


def updateMessage(updateMsg, tgUserId):
    
    isTester = fs.isTester(tgUserId)
    
    fileId = fs.getCurrentFileId(tgUserId)
    tgFileId, fileName = fs.getTelegramFileIdAndFileNameById(tgUserId, fileId)
    fullPath = fs.getFullPath(tgUserId, fileId)
    
    if tgFileId:
        #File
        buttons = [[
            Buttons.getDeleteButton(fileId),
            Buttons.getCutButton(fileId),
            Buttons.getRenameButton(fileName)
        ],[
            Buttons.getBackButton(),
            Buttons.getHomeButton()
        ]]
        
        if isTester:
            buttons.append([
            ])
            
        if updateMsg:
            # Single File, update Message
            
            for t in ['document', 'photo', 'audio','video', 'animation']:
                info = api.editMessageMedia(
                    chat_id=tgUserId,
                    mediaType=t,
                    media=tgFileId,
                    message_id=updateMsg,
                    button_array_array=buttons,
                    caption=fullPath)
                # msgAdmin("info")
                # msgAdmin(info)
                if info[0]:
                    return info
                
                # if info[0] or info[1].count('are exactly the same'):
                #     return info
                    
                if info and not info[1].count('type of file mismatch'):
                    msgAdmin("Single File, update Message failed")
                    msgAdmin(info)
            
            # voice after else
            info = api.sendVoice(
                chat_id=tgUserId,
                voice=tgFileId,
                caption=fullPath,
                button_array_array=[[Buttons.getDeleteButton(fileId)]])
            if info[0]:
                return info
            
            if not info[1].count('type of file mismatch'):
                msgAdmin("Single File, update Message failed")
                msgAdmin(info)
        
        # else:
        # Single File, new Message
        info = api.sendDocument(
            chat_id=tgUserId,
            document=tgFileId,
            caption=fullPath,
            button_array_array=buttons)
        if info[0]:
            return info
            
        info = api.sendPhoto(
            chat_id=tgUserId,
            photo=tgFileId,
            caption=fullPath,
            button_array_array=buttons)
        if info[0]:
            return info
            
        
        
        msgAdmin("Single File new Message failed")
        msgAdmin(info)
        
    else:
        #Folder
        buttons = []
        photo=BG_PIC
        
        folderContent = fs.getFolderContent(tgUserId, fileId)

      
        # dont rewrite fileId, fileName!!!
        for f_id, f_name, tg_f_id in folderContent:
            buttons.append(
                [Buttons.getButton(f_name, '/file ' + str(f_id))])

        if fileId:
            #subfolder
            if (len(buttons) < 1):
                photo=EMPTY_SKY
                buttons.append([Buttons.getDeleteButton(fileId)])
            
            buttons.append([
                Buttons.getNewFolderButton(),
                Buttons.getPasteButton(fileId),
                Buttons.getRenameButton(fileName)
            ])
            buttons.append([
                Buttons.getUpButton(),
                Buttons.getHomeButton()
            ])
        else:
            #root folder
            buttons.append([
                Buttons.getNewFolderButton(),
                Buttons.getButton("Clipboard coming soon", "/")
            ])
            buttons.append([
                Buttons.getDonateButton(),
                Buttons.getButton("Settings coming soon","/"),
                Buttons.getBotlistButton()
            ])
            
        # if (len(buttons) < 1):
        #     photo=EMPTY_SKY
        #     buttons.append([Buttons.getDeleteButton(fileId)])
            
        # sortbuttons
        if len(buttons) > 3:
            buttons.insert(0, [
                Buttons.getSortDateButton(),
                Buttons.getSortNameButton()
            ])
    
        caption = ("Files in Folder %s:" % (fullPath, ))
        return sendPhoto(
            updateMsg,
            tgUserId=tgUserId,
            photo=photo,
            caption=caption,
            button_array_array=buttons)

# api.setMyCommands

def printSuggestions(tgUserId):
    suggs = fs.getSuggestions()
    butts = [[]]
    for s_id, voteCount, text, creator in suggs:
        butts.append([Buttons.getButton("⬇️  %s (%s Votes)  ⬇️"%(text,voteCount), "/")])
        if tgUserId==creator:
            butts.append([Buttons.getButton("🗑 Remove", "/unsuggest")])
        else:
            butts.append([Buttons.getVoteUpButton(s_id) , Buttons.getVoteDownButton(s_id)])
            
    butts.append([Buttons.getInlineButton("Submit own", "/suggest ")])
    sendMessage(tgUserId, "Suggestions (votes are secret):",butts)

def handleBotCommand(updateMsg, tgUserId, cmd, halfString=None):
    
    isTester = fs.isTester(tgUserId)
    
    cmd = cmd.split()[0]
    halfString = str(halfString).strip()
    
    if ("/start" == cmd) or ("/home" == cmd):
        fs.addUser(tgUserId)
        fs.setCurrentFolder(tgUserId, None)
        return updateMessage(updateMsg, tgUserId)
        
    # admin
    
    elif "/_cmds" == cmd:
        api.setMyCommands([
            {"command":"start","description":"Home Screen"},
            {"command":"ls","description":"List Files Again"},
            {"command":"reset","description":"Delete All Files"},
            {"command":"donate","description":"Buy me Donuts"},
            {"command":"newfolder","description":"Create a new Folder"},
            {"command":"suggestions","description":"List update suggestions"},
            {"command":"rename","description":"Rename Current Folder"}
        ])
    
    elif "/_f" == cmd:
        dump = fs._dumpFile(tgUserId, halfString)
        sendMessage(tgUserId, dump)
        return
    
    elif ("/_dump" == cmd) or("/_u" == cmd):
        if fs.isAdmin(tgUserId):
            dump = fs.dumpUser(halfString)
            sendMessage(tgUserId, dump)
            return
        
    elif "/_announce" == cmd:
        return
        rows = fs._getAllUsers(tgUserId,msgAdmin)
        counter = 0
        for us_id_row in rows:
            us_id = us_id_row[0]
            sendMessage(us_id, halfString)
            counter += 1
        sendMessage(tgUserId, "announced %s people"%counter)
        return
    
    elif "/_announce_tester" == cmd:
        rows = fs._getAllUsers(tgUserId,msgAdmin)
        counter = 0
        for us_id_row in rows:
            us_id = us_id_row[0]
            if fs.isTester(us_id):
                sendMessage(us_id, halfString)
                counter += 1
        sendMessage(tgUserId, "announced %s people"%counter)
        return
    
    elif "/_delete_file" == cmd:
        fs._deleteFile(tgUserId, halfString)
        return updateMessage(updateMsg, tgUserId)
        
    elif "/_moveHome" == cmd:
        fs._moveHome(tgUserId, halfString)
        return updateMessage(updateMsg, tgUserId)
        
    elif "/_premium" == cmd:
        fs._makePremium(tgUserId, halfString)
        sendMessage(tgUserId, "made %s promium"%halfString)
        sendMessage(halfString, "You are now promium") 
        return
    
    elif "/_unpremium" == cmd:
        fs._makePremium(tgUserId, halfString, False)
        sendMessage(tgUserId, "removed %s promium"%halfString)
        return
    
    
    elif "/_0new_folder" == cmd:
        folderName = halfString
        currentFolder = fs.getCurrentFolderId(0)
        fs._createFolder(tgUserId, 0, folderName, currentFolder)
        
    elif "/_0cd" == cmd:
        folderId = halfString
        fs._setCurrentFolder(tgUserId, 0, folderId)
    
    # normal user
    
    elif "/ls" == cmd:
        return updateMessage(updateMsg, tgUserId)
    
    elif "/document" == cmd:
        api.sendDocument(tgUserId, halfString, caption=None, button_array_array=[[Buttons.getDeleteMessageButton()]])
    
    elif "/suggest" == cmd:
        fs.unSuggest(tgUserId)
        if halfString and halfString.strip():
            fs.suggest(tgUserId, halfString)
            sendMessage(
                tgUserId,
                "suggestion registered",
                [[Buttons.getButton("Undo", "/unsuggest"),Buttons.getShowSuggestionsButton()]]
            )
        return
    
    elif "/unsuggest" == cmd:
        fs.unSuggest(tgUserId)
        sendMessage(tgUserId, "unsuggestion registered",[[Buttons.getShowSuggestionsButton()]])
        return
    
    elif "/suggestions" == cmd:
        printSuggestions(tgUserId)
        return
        
    elif "/vote_up" == cmd:
        api.deleteMessage(tgUserId, updateMsg)
        fs.voteSuggestion(tgUserId, halfString, 1)
        printSuggestions(tgUserId)
        return
        
    elif "/vote_down" == cmd:
        api.deleteMessage(tgUserId, updateMsg)
        fs.voteSuggestion(tgUserId, halfString, -1)
        printSuggestions(tgUserId)
        return
    
    elif "/delete_msg" == cmd:
        return api.deleteMessage(tgUserId, updateMsg)
    elif "/sort_name" == cmd:
        fs.setSortBy(tgUserId,name=True)
        return updateMessage(updateMsg, tgUserId)
    elif "/sort_date" == cmd:
        fs.setSortBy(tgUserId,name=False)
        return updateMessage(updateMsg, tgUserId)
        
    elif "/collect" == cmd:
        newParent = fs.getCurrentFolderId(tgUserId)
        fs.collectWorkspace(tgUserId, newParent)
        return updateMessage(updateMsg, tgUserId)
    elif "/cut" == cmd:
        fileId = halfString
        fs.unTieFile(tgUserId, fileId)
        return updateMessage(updateMsg, tgUserId)
    elif "/ping" == cmd:
        sendMessage(tgUserId, halfString or 'pong')
        return
    elif "/test" == cmd:
        sendMessage(tgUserId, 'You are now Tester [/untest]')
        return
    elif "/untest" == cmd:
        sendMessage(tgUserId, 'You are now UnTester [/test]')
        return
    elif "/dump" == cmd:
        dump = fs.dumpUser(tgUserId)
        sendMessage(tgUserId, dump)
        return
    elif "/f" == cmd:
        fileId = fs.getCurrentFileId(tgUserId)
        sendMessage(tgUserId, fileId or 'Home')
        return
    elif "/id" == cmd:
        sendMessage(tgUserId, tgUserId)
        return
    elif "/tf" == cmd:
        fileId = fs.getCurrentFileId(tgUserId)
        tgFileId = fs.getTelegramFileId(tgUserId,fileId)
        sendMessage(tgUserId, tgFileId)
        return
    elif "/clean" == cmd:
        messy = fs.cleanAbandonedFiles()
        sendMessage(tgUserId, messy)
        return
    elif "/getFile" == cmd:
        fileInfo = api.getFile(halfString)
        sendMessage(tgUserId, fileInfo)
        return
    elif "/stats" == cmd:
        stats = fs.getStats()
        sendMessage(tgUserId, "Users: %s, Total Files: %s"%stats)
        return
    elif "/donate" == cmd:
        sendMessage(tgUserId, DONATE)
        return
    elif "/delete" == cmd:
        fileId = halfString
        fileName = fs.getFileNameById(tgUserId, fileId)
        info = sendPhoto(
            updateMsg=updateMsg,
            tgUserId=tgUserId,
            photo=RED_PIC,
            caption=("Do you really want to delete %s?" % fileName),
            button_array_array=[[
                Buttons.getDeleteYesButton(fileId),
                Buttons.getNoButton()
            ]])
        if not info[0]:
            msgAdmin("sendPhoto failed")
            msgAdmin(info)
        return info
    elif "/delete_yes" == cmd:
        fs.moveUp(tgUserId)
        fs.deleteFile(tgUserId, halfString)
        return updateMessage(updateMsg, tgUserId)
    elif "/cd_dot_dot" == cmd:
        fs.moveUp(tgUserId)
        return updateMessage(updateMsg, tgUserId)
    elif "/cd_root" == cmd:
        fs.setCurrentFolder(tgUserId, None)
        return updateMessage(updateMsg, tgUserId)
    elif ("/cdls" == cmd) or ("/file" == cmd):
        fs.setCurrentFolder(tgUserId, halfString)
        return updateMessage(updateMsg, tgUserId)
    elif "/newfolder" == cmd:
        folderId = fs.getCurrentFolderId(tgUserId)
        fs.createFolder(tgUserId, halfString, folderId)
        return updateMessage(updateMsg, tgUserId)
    
    elif "/rename" == cmd:
        fileId = fs.getCurrentFileId(tgUserId)
        fs.renameFile(tgUserId, fileId, halfString)
        return updateMessage(updateMsg, tgUserId)
    elif "/reset" == cmd:
        return sendPhoto(
            updateMsg=updateMsg,
            tgUserId=tgUserId,
            photo=RED_PIC,
            caption=("Do you really want to delete all your files?"),
            button_array_array=[[
                Buttons.getResetYesButton(),
                Buttons.getNoButton()
            ]])
    elif "/reset_yes" == cmd:
        fs.resetUser(tgUserId)
        return updateMessage(updateMsg, tgUserId)
    elif "/botlist" == cmd:
        sendMessage(tgUserId, BOTS_ARCHIVE_LINK)
        return
    
    elif "/" == cmd:
        return
    else:
        msgAdmin("else")
        msgAdmin(cmd)
        return (None, None, None)
        
    return ("You can remove previous message",)


def handleSearch(chat_id, searchString):
    rows = fs.searchFileByName(chat_id, searchString)
    if rows:
        buttonsArrayArray = []
        for f_ids in rows:
            f_id = f_ids[0]
            fullPath = fs.getFullPath(chat_id, f_id)
            buttonsArrayArray.append([Buttons.getButton(fullPath,"/cdls %s"%f_id)])
        buttonsArrayArray.append([Buttons.getHomeButton()])
        sendPhoto(None, chat_id, BG_PIC, "Results for %s:"%searchString, buttonsArrayArray)
    else:
        sendPhoto(None, chat_id, EMPTY_SKY, "No results for %s"%searchString, [[Buttons.getHomeButton()]])
        


def getUrlsInMessage(message):
    if not 'entities' in message:
        return None
    entities = message['entities']
    urls = []
    for e in entities:
        if 'url' == e['type']:
            text = message['text']
            offset = e['offset']
            length = e['length']
            url = text[offset:offset + length]
            halfString = text[offset + length:]
            urls.append((url, halfString))
    return urls

def getCmdsInMessage(message):
    if not 'entities' in message:
        return None
    entities = message['entities']
    cmds = []
    for e in entities:
        if 'bot_command' == e['type']:
            text = message['text']
            offset = e['offset']
            length = e['length']
            cmd = text[offset:offset + length]
            halfString = text[offset + length:]
            cmds.append((cmd, halfString))
    return cmds

# Buttons (only?)
def handleCallbackQuery(callback_query):
    if 'data' in callback_query and 'message' in callback_query:
        callback_query_id = callback_query['id']

        message = callback_query['message']
        message_id = message['message_id']
        chat = message['chat']
        chat_id = chat['id']
        data = callback_query['data'].strip()
        
        fs.setUserMessageId(chat_id, message_id)

        cmd = data.split()[0]
        stringHalf = data[len(cmd):]
        handleBotCommand(message_id, chat_id, cmd, stringHalf)
    
    else:
        
        msgAdmin("No data and message in callback_query")

    api.answerCallbackQuery(callback_query_id)


def handleMessage(message):
    #Non Optional Values
    chat = message['chat']
    message_id = message['message_id']
    chat_id = chat['id']
    
    # msgAdmin('message')
    # msgAdmin(message)
    
    if 'document' in message:
        document = message['document']
        fileName = document['file_name']
        fileId = document['file_id']
        # caption
        currentFolder = fs.getCurrentFolderId(chat_id)
        
        fs.insertFile(chat_id, fileName, fileId, currentFolder)
        api.deleteMessage(chat_id, message_id)
        updateMessage(None, chat_id)
        
    elif 'photo' in message:
        photo = message['photo']
        timestamp = str(time.ctime())
        fileId = photo.pop()['file_id']
        currentFolder = fs.getCurrentFolderId(chat_id)
        
        fs.insertFile(chat_id, '🖼'+timestamp, fileId, currentFolder)
        api.deleteMessage(chat_id, message_id)
        updateMessage(None, chat_id)
        
    elif 'audio' in message:
        audio = message['audio']
        fileId = audio['file_id']
        title = 'title' in audio and audio['title'] or 'Audiofile'
        currentFolder = fs.getCurrentFolderId(chat_id)
        
        fs.insertFile(chat_id, '🎵'+title, fileId, currentFolder)
        api.deleteMessage(chat_id, message_id)
        updateMessage(None, chat_id)
        
    elif 'voice' in message:
        voice = message['voice']
        fileId = voice['file_id']
        date = message['date']
        title = '🎙Voicemessage'+str(date)
        currentFolder = fs.getCurrentFolderId(chat_id)
        
        fs.insertFile(chat_id, title, fileId, currentFolder)
        api.deleteMessage(chat_id, message_id)
        updateMessage(None, chat_id)
        
    elif 'text' in message:
        text = message['text']
        if '@' == text[0]:
            text = text[text.find(" ") + 1]


        # TODO: Merge into getEntities
        bot_commands = getCmdsInMessage(message)
        urls = getUrlsInMessage(message)

        if bot_commands:
            for cmd, halfString in bot_commands:
                info = handleBotCommand(None, chat_id, cmd, halfString)
                # maybe better now
                api.deleteMessage(chat_id, message_id)
                if info:
                    #TODO tries to remove everything
                    # this is unconvenient after /id or so
                    if info[0]:
                        oldMsgId = fs.getUserMessageId(chat_id)
                        if oldMsgId:
                            api.deleteMessage(chat_id, oldMsgId)
                    else:
                        msgAdmin("api.send? error")
                        msgAdmin(info)
        elif urls:
            for url, halfString in urls:
                ping = api.sendDocument(chat_id, document=url, caption=None, button_array_array=[[Buttons.getDeleteMessageButton()]])
                if ping[0]:
                    # msgAdmin(ping[1].json())
                    pong = ping[1].json()['result']
                    handleMessage(pong)
                    api.deleteMessage(chat_id, message_id)
                    
                
        else:
            #plain text
            api.deleteMessage(chat_id, message_id)
            results = handleSearch(chat_id, text)
            oldMsgId = fs.getUserMessageId(chat_id)
            if oldMsgId:
                api.deleteMessage(chat_id, oldMsgId)

