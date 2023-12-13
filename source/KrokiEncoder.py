import base64
import zlib
import requests


class KrokiEncoder:
    def __init__(self,
                 file_path,
                 diagram_type,
                 output_img_extension) -> None:
        self._file_path = file_path
        self._extension = output_img_extension
        self._diagram_type = diagram_type
        self._kroki_url = self._text_diagram_to_kroki_url(
            self.file_path,
            self.diagram_type,
            self.extension)
        self._response = self._send_get_request(self._kroki_url)

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
        with open(file_path, "r") as text_file:
            url_based64: str = base64.urlsafe_b64encode(
                zlib.compress(
                    text_file.read().encode('utf-8'), 9)).decode('ascii')
        return f"https://kroki.io/{diagram_type}/{extension}/{url_based64}"

    def _send_get_request(self, kroki_url: str) -> requests:
        """send GET requests to kroki API

        Args:
            kroki_url (str): kroki URL contains diagram type, expected image extension, based64 text string

        Returns:
            requests: response from Kroki API
        """
        return requests.get(kroki_url)

    def export_image(self, image_path: str) -> None:
        """write kroki response to file.

        Args:
            image_path (str): path to image file which will be written in.
        """
        with open(image_path, "wb") as image_file:
            image_file.write(self._response.content)


def main() -> int:
    return 0


if __name__ == "__main__":
    main()

# Author: Anh-Minh Do, 12.2023, Potsdam, Germany
# License: MIT