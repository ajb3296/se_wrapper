import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .enums import *
from .error import *

class Seboard:
    def __init__(self):
        self.DOMAIN = "https://seboard.site"

        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        self.accessToken = None
        self.refreshToken = None
    
    def login(self, id: str, pw: str):
        """ 로그인을 수행합니다.

        id: 로그인에 사용할 ID
        pw: 로그인에 사용할 비밀번호 """
        tokens = requests.post(f"{self.DOMAIN}/v1/formLogin", data={"username": id, "password": pw}).json()

        if tokens.get("code") == 106:
            raise LoginError("사용자 정보가 일치하지 않습니다")
        self.accessToken = tokens["accessToken"]
        self.refreshToken = tokens["refreshToken"]

        self.header["Authorization"] = f"Bearer {self.accessToken}"

    def logout(self):
        """ 로그아웃을 수행합니다 """
        requests.post(f"{self.DOMAIN}/v1/logoutProc",
                            headers=self.header,
                            json={"refreshToken": self.refreshToken}
        )

    def write_post(self, title: str, content: str, expose: PostType, password: str = "", anonymous: bool = True) -> bool:
        """ 게시글을 작성합니다.

            title: 글 제목
            expose: 비밀글 여부
            password: 비밀글일 경우 열람할 수 있는 비밀번호를 입력해야 함
            anonymous: 익명 여부(기본값: 익명) """
        
        if expose != PostType.PRIVACY:
            password == ""
        result = requests.post(f"{self.DOMAIN}/v1/posts",
                        headers=self.header,
                        json={"title": title,
                              "contents": content,
                              "categoryId": 4,
                              "pined": False,
                              "exposeOption":{"name": expose.value,
                                              "password": password},
                              "attachmentIds":[],
                              "anonymous": anonymous,
                              "isSyncOldVersion":False})
        
        return result.status_code == 201
    
    def delete_post(self, post_id: int) -> bool:
        """ 게시글 id를 입력하면 해당 게시글을 제거합니다.
            
            post_id: 제거할 게시글 아이디 """
        result = requests.delete(f"{self.DOMAIN}/v1/posts/{post_id}",
                        headers=self.header)
        
        return result.status_code == 200
    
    def upload_image(self, image_path: str) -> str:
        """ 이미지를 업로드합니다.

            image_path: 업로드할 이미지 경로 """

        mp_encoder = MultipartEncoder(
            fields = {
                'name': "files",
                'filename': image_path.split("/")[-1],
                'files': (os.path.basename(image_path), open(image_path, 'rb'), 'image')
            }
        )

        result = requests.post(f"{self.DOMAIN}/v1/files",
                                  headers=self.header | {'Content-Type': mp_encoder.content_type},
                                  data=mp_encoder)
        
        if result.status_code != 200:
            raise UploadError("이미지 업로드에 실패하였습니다")
        
        return result.json()["url"]

# 테스트 코드
if __name__ == "__main__":
    if os.path.exists(".env"):
        from dotenv import load_dotenv
        load_dotenv()

        id = os.environ.get('id')
        password = os.environ.get('password')

        seboard = Seboard()
        seboard.login(id, password)
        # seboard.upload_image("1204.png")
        # seboard.write_post("test", "<p>test</p>", PostType.PRIVACY, "1234")
        seboard.logout()
    
    else:
        print("환경변수 파일이 존재하지 않습니다")