from models import *

workers = {}
time_slots = {}
time_slot_list = []

with open('data.txt', 'r') as f:
  data = f.readline().split()
  prev_id = None
  for id in data[1:]:
    str_id = str(id)
    time_slots[str_id] = TimeSlot(str_id)
    if (prev_id):
      time_slots[prev_id].slot_after = time_slots[str_id]
      time_slots[str_id].slot_before = time_slots[prev_id]
    prev_id = str_id

  f.readline()

  for line in f:
    data = line.split() #time name pref
    time, name, pref = data[0], data[1], int(data[2])

    if (not name in workers):
      workers[name] = Worker(name)
    workers[name].update_pref(time, pref)
    if not pref == 0:
      time_slots[time].add_worker(workers[name])


time_slot_list = dict_val_to_list(time_slots)

# Sort time_slot_list by number of avaialbe workers in increasing order
time_slot_list.sort(key=lambda x: x.number_of_workers)

# sort worker lists of each time slot
sort_all_time_slots(time_slots)

for time_slot in time_slot_list:
  if not time_slot.worker and time_slot.available_workers:
    worker = time_slot.get_worker()
    if worker:
      if not worker.can_work():
        while time_slot.available_workers:
          alt_worker = time_slot.get_worker()
          if alt_worker.can_work:
            worker = alt_worker
            break
      time_slot.assign_worker(worker)
      assign_adj_time_slots(time_slot, worker)


print_result(time_slot_list, workers)


