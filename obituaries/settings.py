BOT_NAME = "obituaries"

SPIDER_MODULES = ["obituaries.spiders"]
NEWSPIDER_MODULE = "obituaries.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "obituaries.pipelines.ObituariesPipeline": 300,
}
