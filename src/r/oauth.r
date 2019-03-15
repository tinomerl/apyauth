library(httr)

authUrl = "https://app.hubspot.com/oauth/authorize"
tokenUrl = "https://api.hubapi.com/oauth/v1/token"
analyticsBase = "https://api.hubapi.com/analytics/v2/reports"

clientId = "6861bfc7-f088-4720-a689-e49030fe8e44"
clientSecret = "d603bb1e-1435-4ece-b11c-6be56ca31ad4"

app = oauth_app("hubspot",clientId, clientSecret)

hubspot = oauth_endpoint(authorize = authUrl, access = tokenUrl)

token = oauth2.0_token(hubspot,app, scope = c("business-intelligence"))

tkn = token[["credentials"]][["access_token"]]

breakdown = "sessions"
timeperiod = "weekly"
start = "20190101"
end = "20190131"

breakTimeUrl = paste(analyticsBase,breakdown,timeperiod, sep = "/")
reqUrl = paste0(breakTimeUrl,"&start=",start,"&end=",end)

resp = GET(reqUrl,add_headers(Authorization = paste("Bearer", tkn, sep = " "), `Content-Type` = "application/json"))

contacts = GET("https://api.hubapi.com/contacts/v1/lists/all/contacts/all", ,add_headers(Authorization = paste("Bearer", tkn, sep = " ")))

View(resp)