import datetime
import os
import random
import socket
import string
from typing import Dict, List
import webbrowser

from dateutil import tz
import requests


class Oauth2Session:
    def __init__(
        self,
        name: str,
        client_id: str,
        client_secret: str,
        authorize_url: str,
        access_token_url: str,
        refresh_token_url: str = "",
        access_token: str = "",
        refresh_token: str = "",
        scope: List = [],
        redirect_uri: str = "http://localhost:1410/",
        params: Dict = {},
    ) -> None:
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorize_url = authorize_url
        self.access_token_url = access_token_url
        self.refresh_token_url = refresh_token_url
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.params = params
        self.expiry_date: datetime.datetime = datetime.datetime(
            1970, 1, 1, 0, 0, 0
        ).replace(tzinfo=tz.tzlocal())

    def request_token(self):
        if self.refresh_token != "":
            response = self.generate_refresh_token(
                refresh_token_url=self.refresh_token_url,
                refresh_token=self.refresh_token,
                client_id=self.client_id,
                client_secret=self.client_secret,
            )
        if self.refresh_token == "":
            response = self.generate_access_token(
                self.access_token_url,
                self.authorize_url,
                self.client_id,
                self.client_secret,
                self.redirect_uri,
                self.scope,
                self.params,
            )

        response_date = response.headers.get("Date")
        expires_in = response.json().get("expires_in")
        self.expiry_date = self.calc_expiry_date(response_date, expires_in)

    def create_page(self):
        """
        Creates a simple HTML Page.

        The Page created is just to show the user that he can now return to the console.
        """
        htmlFile = "index.html"
        f = open(htmlFile, "w")
        f.write(
            "<html><body><p>Python has created this Page for the Authentication. It can now be closed.</p></body></html>"
        )
        f.close()
        return htmlFile

    def get_code(self, url: str, params: Dict):
        """
        Calls port_listen. Processes Parameters.

        Keyword Arguments:\n
        authUrl -- The Authentication URL added with Parameters.
        state -- The generated State Parameter to check if the Session is still the same

        It reads all the parameters from the response and turns them into a dictionary. Exits if the state differs.

        Returns:\n
        Code Parameter send from the authentication Server.
        """
        auth_params: str = "&".join([f"{key}={value}" for key, value in params.items()])
        webbrowser.open(f"{url}?{auth_params}")
        res = self.port_listen()
        res = res.decode("utf-8").splitlines()
        res = res[0]
        res_params = res[res.find("?") + 1 : res.find("HTTP") - 1]
        params_list = res_params.split("&")
        params_dict = {}
        for i in params_list:
            key, val = i.split("=")
            params_dict.update({key: val})

        if params["state"] != params_dict["state"]:
            raise Exception("Session Error state is not valid")

        code = params_dict.get("code")
        return code

    def port_listen(self):
        """
        Opens a port and Listens to Response.

        The method opens a socket on http://localhost:1410/ creates a webpage and catches the Response. When it registers an incoming session the socket is closed. It also deletes the created HTML Page.
        Returns:\n
        The received Information on the port.
        """
        host = "localhost"
        port = 1410
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)
        print("Started Listening")
        print("Waiting for Connection on port 1410 on localhost")
        ressock, addr = sock.accept()
        req = ressock.recv(1024)
        filename = self.create_page()
        f = open(filename, "r")
        ressock.sendall(str.encode("HTTP/1.0 200 OK\n", "iso-8859-1"))
        ressock.sendall(str.encode("Content-Type: text/html\n", "iso-8859-1"))
        ressock.send(str.encode("\r\n"))
        for i in f.readlines():
            ressock.sendall(str.encode(i, "iso-8859-1"))
        f.close()
        ressock.close()
        os.unlink(filename)
        return req

    def generate_access_token(
        self,
        access_token_url: str,
        authorize_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: List,
        params: Dict,
    ):
        """
        This function gets the Access Token and saves it.

        Keyword Arguments:\n
        scope -- scope needed for the Authentication.\n
        additionalParams -- Extra Parameters needed by the Auth Server. Needs to be defined as a dictionary.

        The Function calls the authUrlBuild and overhands the constructed URL to the get_code Function to receive the code needed for the Access Token.
        Afterwards it calls the token Endpoint and exchanges the code for a token.
        It also asks you if you wanna save the token between sessions and constructs a file with the given service/app name in which the token is stored.

        Returns:\n
        Access Token from the Response
        """
        state = "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(50)
        )

        auth_params: dict = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "response_type": "code",
            "scope": "%20".join(scope),
        }
        auth_params.update(params)
        code = self.get_code(authorize_url, auth_params)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        ans = requests.post(access_token_url, data=data, headers=headers)
        status_code = ans.status_code
        if status_code != 200:
            get_params: dict = {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "response_type": "code",
            }
            ans = requests.get(access_token_url, params=get_params)

        content: Dict = ans.json()
        self.refresh_token = content.get("refresh_token")
        self.access_token = content.get("access_token")
        return ans

    def generate_refresh_token(
        self,
        refresh_token_url: str,
        refresh_token: str,
        client_id: str,
        client_secret: str,
    ):
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
        data = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        }
        ans = requests.post(refresh_token_url, data=data, headers=headers)
        content: Dict = ans.json()
        self.access_token = content.get("access_token")
        return ans

    def calc_expiry_date(self, response_date, expires_in):
        """
        Calculates the Expirydate of the Access Token.

        Keyword Arguments: \n
        respDate -- Date taken out of the Header of the Response.\n
        expiresIn -- Seconds in which the Acces Token expires in taken out of the content of the Response.

        It Adds the expiresIn to the respDate and calculates the local Time at which the Access Token will expire.

        Returns:\n
        Expiry Date of Access Token (Date)
        """
        expiry_date = datetime.datetime.strptime(
            response_date, "%a, %d %b %Y %H:%M:%S GMT"
        ) + datetime.timedelta(seconds=expires_in)
        fromtz = tz.tzutc()
        totz = tz.tzlocal()
        expiry_date = expiry_date.replace(tzinfo=fromtz).astimezone(totz)
        return expiry_date

    def validate_access_token(self):
        now = datetime.datetime.now(tz=tz.tzlocal())
        if now >= self.expiry_date:
            print("Token invalid")
            return False
        return True
