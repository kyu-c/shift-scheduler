import random, sys
MAX_HOURS = 8.25 # targeted hours per worker
MIN_SHIFT_HOURS = 1 # minimum hours of a shift
MAX_SHIFT_HOURS = 4 # maximum hours of a shift

# Unit 30 mins
MAX_SLOTS =  MAX_HOURS * 2
MIN_SHIFT_SLOTS = MIN_SHIFT_HOURS * 2
MAX_SHIFT_SLOTS = MAX_SHIFT_HOURS * 2

class TimeSlot:
  def __init__(self, id):
    self.id = id
    self.available_workers = []
    self.worker = None
    self.slot_after = None
    self.day = id[:3]
    self.sorted = False

  def __repr__(self):
    return "TimeSlot(" + self.id +")"

  def add_worker(self, worker):
    self.available_workers.append(worker)

  # Should be used after available_workers list is sorted
  def get_worker(self):
    if self.sorted == False:
      self.sort()
    if self.available_workers:
      highest_pref = self.available_workers[0].preference[self.id]
      worker_slots = self.available_workers[0].slots
      worker_index = 0
      for i in range(len(self.available_workers)):
        if highest_pref - random.randint(0,1) < self.available_workers[i].preference[self.id]:
          break
        elif worker_slots - random.randint(0,2) > self.available_workers[i].slots:
          worker_slots = self.available_workers[i].slots
          worker_index = i

      return self.available_workers.pop(worker_index)

  def assign_worker(self, worker):
    self.worker = worker
    worker.slots += 1

  # Sort available workers by preference (high preference to low)
  def sort(self):
    self.available_workers.sort(key=lambda x: x.preference[self.id], reverse=True)
    self.sorted = True


class Worker:
  def __init__(self, id):
    self.id = id
    self.slots = 0
    self.preference = {}
    self.work_days = set()

  def __repr__(self):
    return self.id

  def update_pref(self, time_slot_id, pref):
    self.preference[time_slot_id] = pref

  def get_pref(self, time_slot_id):
    return self.preference[time_slot_id]

  def update_work_days(self, day):
    self.work_days.add(day)

  def can_work(self, time_slot):
    return self.slots < MAX_SLOTS and not (time_slot.day in self.work_days)

### other functions
def get_shift(start_time_slot, worker):
  shift = [start_time_slot]
  slot_after = start_time_slot.slot_after
  duration = 1
  while (duration < MAX_SHIFT_SLOTS and slot_after
        and duration + worker.slots <= MAX_HOURS *2):
    pref_after = worker.get_pref(slot_after.id)
    if pref_after > 0:
      shift.append(slot_after)
      slot_after = slot_after.slot_after
      duration += 1
    else:
      break
  return shift

def assign_shift(shift, worker):
  worker.update_work_days(shift[0].day)
  for time_slot in shift:
    time_slot.assign_worker(worker)

def get_min_max_worker_slots_diff(workers):
  slots = [workers[key].slots for key in workers]
  min_slots = min(slots)
  max_slots = max(slots)
  return max_slots - min_slots

def get_num_uncovered_shifts(time_slots):
  num_uncovered = 0
  for time_slot in time_slots:
    if time_slot.worker is None:
      num_uncovered += 1
  return num_uncovered

def print_result(time_slots, workers, output):
  hours = {}
  with open(output, 'w') as f:
    for time_slot in time_slots:
      worker = str(time_slot.worker)
      f.write(time_slot.id + " " + worker + "\n")
      if worker in hours:
        hours[worker] += 0.5
      else:
        hours[worker] = 0.5

  print "====Summary===="
  for worker in hours:
    print worker + " - Hours: " + str(hours[worker])
