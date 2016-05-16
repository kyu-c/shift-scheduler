import csv, sys, argparse, random, copy
from models import *
from util import *

def get_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument("input", help="input.csv")
  parser.add_argument("output", help="output.csv")
  parser.add_argument("-i", "--iterations", type=int, default=1000,
                      help="Number of iterations")
  return parser.parse_args()

def schedule_shifts(headers, rows):
  workers = {}
  time_slots = {}
  time_slot_list = []

  for name in headers[1:]:
    workers[name] = Worker(name)

  prev_id = None
  for row in rows:
    current_id = row["time"]
    update_dict(time_slots, current_id, TimeSlot(current_id))
    if (prev_id and time_slots[prev_id].day == time_slots[current_id].day):
      time_slots[prev_id].slot_after = time_slots[current_id]

    for name in workers:
      pref = int(row[name])
      worker = workers[name]
      worker.update_pref(current_id, pref)
      if pref > 0:
        time_slots[current_id].add_worker(worker)

    prev_id = current_id

  priority = range(1,7)
  days = ["MON", "TUE", "WED", "THU", "FRI", "SUN"]
  random.shuffle(days)
  days = dict(zip(days, priority))
  time_slot_list = dict_val_to_list(time_slots)
  time_slot_list.sort(key=lambda ts: (days[ts.day], ts.time))

  for time_slot in time_slot_list:
    if not time_slot.worker and time_slot.available_workers:
      while time_slot.available_workers:
        worker = time_slot.get_worker()
        if worker.can_work(time_slot):
          shift = get_shift(time_slot, worker)
          if len(shift) >= MIN_SHIFT_SLOTS:
            break

      if worker:
        duration = len(shift)
        if duration > MAX_SHIFT_SLOTS - 3:
          duration = random.randrange(5, duration + 1)
        assign_shift(shift[:duration], worker)

  days = {"MON": 1, "TUE": 2, "WED": 3, "THU": 4, "FRI": 5, "SUN": 6}
  time_slot_list.sort(key=lambda ts: (days[ts.day], ts.time))

  res = {"time_slots": time_slot_list, "workers": workers}
  return res

def repeat_scheduling(headers, rows, iterations):
  best_schedule = schedule_shifts(headers, rows)
  best_uncovered = get_num_uncovered_shifts(best_schedule["time_slots"])
  best_slots_diff = get_min_max_worker_slots_diff(best_schedule["workers"])

  for i in xrange(iterations):
    current_schedule = schedule_shifts(headers, rows)
    current_uncovered = get_num_uncovered_shifts(current_schedule["time_slots"])
    current_slots_diff = get_min_max_worker_slots_diff(current_schedule["workers"])
    if current_uncovered <= best_uncovered and current_slots_diff <= best_slots_diff:
      best_schedule = current_schedule
      best_uncovered = current_uncovered
      best_slots_diff = current_slots_diff

  return best_schedule

if __name__ == '__main__':
  args = get_arguments()
  headers = get_headers(args.input)
  rows = get_list_of_dicts(args.input)
  iterations = int(args.iterations)
  schedule = repeat_scheduling(headers, rows, iterations)
  write_result(schedule["time_slots"], args.output)
  print_summary(schedule["workers"])
