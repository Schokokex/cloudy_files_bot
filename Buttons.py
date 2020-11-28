def getButton(text, callback_data):
    return {"text": text,"callback_data": callback_data}

def getInlineButton(text, switch_inline_query_current_chat):
    return {"text": text,"switch_inline_query_current_chat": switch_inline_query_current_chat}

def getReplyMarkup(buttons_array_array):
    return {"inline_keyboard":buttons_array_array}

def getBackButton():
    return getButton("⬅️ Back","/cd_dot_dot")

def getUpButton():
    return getButton("⬆️ Up", "/cd_dot_dot")

def getHomeButton():
    return getButton("🏠 Home", "/cd_root")

def getDonateButton():
    return getButton("💵 Donate", "/donate")

def getBotlistButton():
    return getButton("⭐️Rate", "/botlist")

def getNewFolderButton():
    return getInlineButton("🗂 New", "/newfolder 🗂New_Folder")

def getDownloadButton(file_id):
    return getButton("⬇️ Download","/download " + str(file_id))

def getRenameButton(old_name):
    return getInlineButton("✍️ Rename", "/rename " + str(old_name))

def getDeleteButton(folderId):
    return getButton("🗑 Delete", "/delete " + str(folderId))

def getDeleteYesButton(fileId):
    return getButton("⚠️ Yes","/delete_yes " + str(fileId))

def getResetYesButton():
    return getButton("⚠️ Yes", "/reset_yes")

def getDeleteNoButton():
    return getButton( "No", "/ls")

def getNoButton():
    return getButton( "No", "/ls")

def getSortDateButton():
    return getButton("Date 🔽", "/sort_date")

def getSortNameButton():
    return getButton("Name 🔽", "/sort_name")

def getCutButton(fileId):
    return getButton( "⏩🏠 Drop","/cut " + str(fileId))

def getPasteButton(fileId):
    return getButton( "🏠⏩ Collect", "/collect " + str(fileId))

def getDeleteMessageButton():
    return getButton( "❌", "/delete_msg")

def getVoteUpButton(vote_id):
    return getButton("➕",  "/vote_up %s"%vote_id)

def getVoteDownButton(vote_id):
    return getButton("➖", "/vote_down %s"%vote_id)

def getShowSuggestionsButton():
    return getButton("🗳 Show List","/suggestions")

