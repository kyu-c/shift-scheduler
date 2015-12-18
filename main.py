from models import *
import csv, random, copy


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

  time_slot_list = dict_val_to_list(time_slots)
  time_slot_list.sort(key=lambda x: x.id)

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

  return (copy.copy(time_slot_list), copy.copy(workers))


schedules = []
for i in range(10):
  schedules.append(schedule_shifts('sample_data_large.csv'))

for ts_workers in schedules:
  print_result(ts_workers[0], ts_workers[1])
