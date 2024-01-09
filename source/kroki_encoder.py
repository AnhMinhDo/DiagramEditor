import base64
import zlib
import requests


class KrokiEncoder:
    def __init__(self,
                 file_path,
                 diagram_type,
                 output_img_extension) -> None:
        self._file_path: str = file_path
        self._extension: str = output_img_extension
        self._diagram_type: str = diagram_type
        self._kroki_url: str = self._text_diagram_to_kroki_url(
            self.file_path,
            self.diagram_type,
            self.extension)
        self._response: requests.Response = self._send_get_request(self._kroki_url)
        self.status_code: int = self._get_status_code(self._response)
        self.error_message = self._get_error(self._response, self.status_code)

    @property
    def file_path(self) -> str:
        return self._file_path

    @file_path.setter
    def file_path(self, new_path) -> None:
        self._file_path = new_path
        self._kroki_url = self._text_diagram_to_kroki_url(
            self.file_path,
            self.diagram_type,
            self.extension)
        self._response = self._send_get_request(self._kroki_url)
        self.status_code = self._get_status_code(self._response)
        self.error_message = self._get_error(self._response, self.status_code)

    @property
    def extension(self) -> str:
        return self._extension

    @extension.setter
    def extension(self, new_extension: str) -> None:
        self._extension = new_extension
        self._kroki_url = self._text_diagram_to_kroki_url(
            self.file_path,
            self.diagram_type,
            self.extension)
        self._response = self._send_get_request(self._kroki_url)
        self.status_code = self._get_status_code(self._response)
        self.error_message = self._get_error(self._response, self.status_code)

    @property
    def diagram_type(self) -> str:
        return self._diagram_type

    @diagram_type.setter
    def diagram_type(self, new_diagram_type: str) -> None:
        self._diagram_type = new_diagram_type
        self._kroki_url = self._text_diagram_to_kroki_url(
            self.file_path,
            self.diagram_type,
            self.extension)
        self._response = self._send_get_request(self._kroki_url)
        self.status_code = self._get_status_code(self._response)
        self.error_message = self._get_error(self._response, self.status_code)

    def _text_diagram_to_kroki_url(
            self,
            file_path: str,
            diagram_type: str,
            extension: str) -> str:
        """Convert text diagram to kroki_url.

        Args:
            file_path (str): path to file
            diagram_type (str, optional): type of diagram. Defaults to "plantuml".
            extension (str, optional): type of output image. Defaults to "png".

        Returns:
            str: an url with compressed based64 text for the text diagram
        """
        with open(file_path, "r", encoding="utf-8") as text_file:
            url_based64: str = base64.urlsafe_b64encode(
                zlib.compress(
                    text_file.read().encode('utf-8'), 9)).decode('ascii')
        return f"https://kroki.io/{diagram_type}/{extension}/{url_based64}"

    def _send_get_request(self, kroki_url: str) -> requests.Response | None:
        """send GET requests to kroki API

        Args:
            kroki_url (str): kroki URL contains diagram type, expected image extension, based64 text string

        Returns:
            requests.Response: response from Kroki API
        """
        try:
            res = requests.get(kroki_url, timeout=5)
            return res
        except requests.exceptions.ConnectionError:
            return None
            
    def _get_status_code(self, res: requests.Response) -> int | None:
        if res is None:
            return None
        else:
            return res.status_code
        
    def _get_error(self, res: requests.Response, status_code: int) -> None | str:
        if res is None:
            return "Cannot connect to https://kroki.io"
        elif status_code == 400:
            return res.content.decode()
        elif len(res.content) == 0:
            return "Error: HTTP response content is empty. Please re-check diagram type"
        else:
            return None

    def _is_response_body_empty(self, res: requests.Response) -> bool:
        if res is not None:
            return True if len(res.content) == 0 else False

    def export_image(self, image_path: str) -> None:
        """write kroki response to file.

        Args:
            image_path (str): path to image file which will be written in.
        """
        if self.error_message is None:
            with open(image_path, "wb") as image_file:
                image_file.write(self._response.content)
        else:
            print(self.error_message)


def main() -> int:
    return 0


if __name__ == "__main__":
    main()

# Author: Anh-Minh Do, 12.2023, Potsdam, Germany
# License: MIT
    