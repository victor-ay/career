import json


class LinkedInHeaderQueue:
    """
    LinkedInHeaderQue is a header worker manager who is responsible to return header file

    Initiates with <header_map_file.json>
    """
    def __init__(self, header_map_file: str):
        with open(header_map_file, 'r') as fh:
            self._header_map = json.load(fh)

        self._worker_keys = list(self._header_map.keys())
        self._tot_headers_worker = len(self._worker_keys)
        self._current_header_worker_num = 0

    def _validate_exist(self, val_obj):
        if not val_obj:
            raise Exception(f"Object {val_obj} does not exist")

    def _get_next_header_key(self):
        """
        Returns the next worker key for the <header_map_file>
        :return:
        """
        # if not self._worker_keys.get(self._current_header_worker_num):
        #     raise KeyError()
        self._validate_exist(self._worker_keys[self._current_header_worker_num])
        ret_val = self._worker_keys[self._current_header_worker_num]

        if self._current_header_worker_num != self._tot_headers_worker-1:
            self._current_header_worker_num += 1
        else:
            self._current_header_worker_num = 0

        return ret_val

    def get_next_header_file(self):
        """
        Returns next
        :return:
        """
        next_header_key = self._get_next_header_key()
        self._validate_exist(self._header_map[next_header_key].get("headers_json"))
        return self._header_map[next_header_key].get("headers_json")

    def _get_worker_keys(self):
        return self._worker_keys

if __name__ == '__main__':
    headerQ = LinkedInHeaderQueue(header_map_file="../linkedin_scrapper/configs/linkedin_headers_map.json")
    # headerQue = LinkedInHeaderQue(header_map_file="../linkedin_scrapper/configs/headers_files/linkedin_headers_0.json")

    print(headerQ.get_next_header_file())
    print(headerQ.get_next_header_file())
    print(headerQ.get_next_header_file())
    print(headerQ.get_next_header_file())

