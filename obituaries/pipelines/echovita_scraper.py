# ruff: noqa
import json
import os


class EchovitaScraperPipeline:
    def open_spider(self, spider):
        os.makedirs("output", exist_ok=True)
        self.s3_file = open("output/s3_upload.jsonl", "a")
        self.gcs_file = open("output/gcs_upload.jsonl", "a")

    def close_spider(self, spider):
        if hasattr(self, "s3_file"):
            self.s3_file.close()
        if hasattr(self, "gcs_file"):
            self.gcs_file.close()

    def process_item(self, item, spider):
        data = json.dumps(dict(item))

        # S3 upload file
        self.s3_file.write(data + "\n")
        self.s3_file.flush()

        # GCS upload file
        self.gcs_file.write(data + "\n")
        self.gcs_file.flush()

        return item
