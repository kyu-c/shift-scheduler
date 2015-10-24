from models import *
import csv

workers = {}
time_slots = {}
time_slot_list = []

csv_file = open('real_data.csv')
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
      time_slots[current_id].slot_before = time_slots[prev_id]

    for i in range(1, len(row)):
      pref = int(row[i])
      name = headers[i]
      workers[name].update_pref(current_id, pref)
      if pref:
        time_slots[current_id].add_worker(workers[name])

    prev_id = current_id

time_slot_list = dict_val_to_list(time_slots)

# Sort time_slot_list by number of available workers in increasing order
time_slot_list.sort(key=lambda x: x.num_available_workers)

# sort worker lists of each time slot
sort_all_time_slots(time_slots)

for time_slot in time_slot_list:
  if not time_slot.worker and time_slot.available_workers:
    worker = time_slot.get_worker()
    if worker:
      if not worker.can_work(time_slot.day):
        while time_slot.available_workers:
          alt_worker = time_slot.get_worker()
          if alt_worker.can_work(time_slot.day):
            worker = alt_worker
            break
      time_slot.assign_worker(worker)
      worker.update_work_days(time_slot.day)
      assign_adj_time_slots(time_slot, worker)


print_result(time_slot_list, workers)
