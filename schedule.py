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

def schedule_shifts(filename):
  workers = {}
  time_slots = {}
  time_slot_list = []
  csv_file = open(filename)
  csv_reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)

  headers = next(csv_reader, None)

  for name in headers[1:]:
    workers[name] = Worker(name)

  prev_id = None
  for row in csv_reader:
      current_id = row[0]
      update_dict(time_slots, current_id, TimeSlot(current_id))
      if (prev_id and time_slots[prev_id].day == time_slots[current_id].day):
        time_slots[prev_id].slot_after = time_slots[current_id]

      for i in range(1, len(row)):
        pref = int(row[i])
        name = headers[i]
        workers[name].update_pref(current_id, pref)
        if pref:
          time_slots[current_id].add_worker(workers[name])

      prev_id = current_id

  priority = range(1,7)
  days = ["MON", "TUE", "WED", "THU", "FRI", "SUN"]
  random.shuffle(days)
  days = dict(zip(days, priority))
  time_slot_list = dict_val_to_list(time_slots)
  time_slot_list.sort(key=lambda x: (days[x.id[:3]], x.id[4:]))

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
  time_slot_list.sort(key=lambda x: (days[x.id[:3]], x.id[4:]))

  return ((time_slot_list), (workers))

def repeat_scheduling(input, output, iterations):
  best_schedule = schedule_shifts(input)
  best_uncovered = get_num_uncovered_shifts(best_schedule[0])
  best_slots_diff = get_min_max_worker_slots_diff(best_schedule[1])

  for i in xrange(iterations):
    current_schedule = schedule_shifts(input)
    current_uncovered = get_num_uncovered_shifts(current_schedule[0])
    current_slots_diff = get_min_max_worker_slots_diff(current_schedule[1])
    if current_uncovered <= best_uncovered and current_slots_diff <= best_slots_diff:
      best_schedule = current_schedule
      best_uncovered = current_uncovered
      best_slots_diff = current_slots_diff

  print_result(best_schedule[0], best_schedule[1], output)

if __name__ == '__main__':
  args = get_arguments()
  repeat_scheduling(args.input, args.output, int(args.iterations))
