library(httr)

urls = list(
    authUrl = "https://app.hubspot.com/oauth/authorize",
    tokenUrl = "https://api.hubapi.com/oauth/v1/token",
    baseUrl = "https://api.hubapi.com",

    getCalls = list(
        #analytics = "analytics/v2/reports",
        templates = "content/api/v2/templates",
        contacts = "contacts/v1/lists/all/contacts/all",
        emailCampaigns = "email/public/v1/campaigns/by-id",
        blog = "content/api/v2/blogs",
        workflows = "automation/v3/workflows",
        forms = "forms/v2/forms",
        landingpages = "content/api/v2/pages"
    )
)

hubAuth = function() {
    clientId = "6861bfc7-f088-4720-a689-e49030fe8e44"
    clientSecret = "d603bb1e-1435-4ece-b11c-6be56ca31ad4"
    app = oauth_app("hubspot",clientId, clientSecret)
    hubspot = oauth_endpoint(authorize = urls$authUrl, access = urls$tokenUrl)
    token = oauth2.0_token(hubspot,app, scope = c("contacts", "content", "automation", "business-intelligence", "forms"))
    tkn = token[["credentials"]][["access_token"]]
    
    tkn
}


hubCalls = function(tkn) {
    urlEndings = names(urls$getCalls)

    answer = list()
    for (u in urlEndings) {
        print(u)
        url = paste(urls$baseUrl, urls$getCalls[[u]], sep = "/")
        resp = try(GET(url, add_headers(Accept = "application/json", Authorization = paste("Bearer", tkn, sep = " "), `Content-Type` = "application/json")))
        print(resp)
        #data = try(jsonlite::fromJSON(rawToChar(resp$content)))
        if ("try-error" %in% class(data) ) {
            next
        } else {
            answer[[u]] = resp
        }
    }
    answer
}

respToList = function(respList) {
    listNames = names(respList)
    newList = list()
    for (l in listNames) {
        temp = jsonlite::fromJSON(rawToChar(respList[[l]]$content))
        newList[[l]] = temp
    }

    newList
}

tkn = hubAuth()
respList = hubCalls(tkn)
respList = respToList(respList)


contactList = respList$contacts

contactDf = respList$contacts$contacts

row.names(contactDf) = contactDf$properties$firstname

row.names(contactDf) = paste(contactDf$properties$firstname[,1], contactDf$properties$lastname[,1], contactDf$vid, sep = "_")


as.POSIXlt(contactDf$addedAt, origin = "1970-01-01")

View(contactDf$`identity-profiles`)

View(as.data.frame(respList$contacts$contacts$`form-submissions`))