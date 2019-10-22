from apscheduler.schedulers.blocking import BlockingScheduler
from bot import repost

sched = BlockingScheduler()
sched.add_job(repost, "interval", minutes=1)
sched.start()
