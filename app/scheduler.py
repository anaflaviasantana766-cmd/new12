from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import time
from .main import SessionLocal, Book

scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")

async def fetch_and_update():
	# TODO: replace with real scrapers; keeps existing seed for now
	return

def start_scheduler():
	# Every day at 06:00 BRT
	scheduler.add_job(fetch_and_update, "cron", hour=6, minute=0)
	scheduler.start()