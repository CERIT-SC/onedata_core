from oneprovider_client.models.share import Share as OneproviderShare

from onedata_wrapper.converters.abstract_converter import AbstractConverter
from onedata_wrapper.models.share.share import Share


class ShareConverter(AbstractConverter):
    @staticmethod
    def convert(oneprovider_share: OneproviderShare) -> Share:
        # unchanged
        share_id = oneprovider_share.share_id
        name = oneprovider_share.name
        description = oneprovider_share.description
        public_url = oneprovider_share.public_url
        space_id = oneprovider_share.space_id
        root_file_id = oneprovider_share.root_file_id
        root_file_type = oneprovider_share.root_file_type
        handle_id = oneprovider_share.handle_id

        share = Share(share_id=share_id, name=name, description=description, public_url=public_url, space_id=space_id,
                      root_file_id=root_file_id, root_file_type=root_file_type, handle_id=handle_id)
        return share
