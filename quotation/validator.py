import magic

from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError


@deconstructible
class FileValidator:
    error_messages = {
        "file_extension": "無效副檔名: {file_ext}，只能為 {allowed_file_ext}",
        "mime_type": "無效 MIME type: {mime_type}，只能為 {allowed_mime_type}",
        "max_size": "上傳的檔案超過 {max_size}",
        "min_size": "上傳的檔案小於 {min_size}",
    }

    def __init__(self, allowed_extension: tuple, allowed_mime_type: tuple,
                 max_size=None, min_size=None):
        self.allowed_extension = allowed_extension
        self.allowed_mime_type = allowed_mime_type
        self.max_size = max_size
        self.min_size = min_size

    def __call__(self, file):
        file_ext = file.name.split('.')[-1].lower()
        if file_ext not in self.allowed_extension:
            raise ValidationError(
                FileValidator.error_messages["file_extension"].format(
                    file_ext=file_ext,
                    allowed_file_ext=", ".join(self.allowed_extension)))

        mime_type = magic.from_buffer(file.read(), mime=True)
        file.seek(0)

        if mime_type not in self.allowed_mime_type:
            raise ValidationError(
                FileValidator.error_messages["mime_type"].format(
                    mime_type=mime_type,
                    allowed_mime_type=", ".join(self.allowed_mime_type)))

        if self.max_size and file.size > self.max_size:
            raise ValidationError(
                FileValidator.error_messages["max_size"].format(
                    max_size=filesizeformat(self.max_size)))

        if self.min_size and file.size < self.min_size:
            raise ValidationError(
                FileValidator.error_messages["min_size"].format(
                    min_size=filesizeformat(self.min_size)))


@deconstructible
class ItemSnValidator:
    error_messages = {
        "sn_notexisted": "料號: {sn} 不存在",
    }

    def __init__(self, sn_list):
        self.sn_list = sn_list

    def __call__(self, itemsn):
        if itemsn not in self.sn_list:
            raise ValidationError(
                ItemSnValidator.error_messages['sn_notexisted'].format(sn=itemsn)
            )
