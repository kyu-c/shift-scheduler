# Shift-Scheduler
## Synopsis
Shift-Scheduler is an employee shift scheduling program specifically designed for the Instructional Technology Center (ITC) of Haverford College. Given time slots that need to be covered, Shift-Scheduler generates a schedule based on workers' preferences.

## Implementation
Shift-Scheduler uses a randomized greedy algorithm with heuristic in combination with iterative method. It attempts to assign a shift to the worker who prefers the shift the most while balancing the number of hours among workers and ensuring all time slots to be covered.

## Input Format (csv)
A preference of a time slot for a worker is specified from 0 to a certain number, where 0 means unavailability, and higher number means stronger preference.
### Example
time, Amy, Bob, Charles, Dave <br/>
MON-08:30-09:00, 0, 1, 2, 0 <br/>
MON-09:00-09:30, 1, 1, 1, 0 <br/>
MON-09:30-10:00, 1, 2, 0, 0 <br/>
MON-10:00-10:30, 2, 2, 0, 3 <br/>
MON-10:30-11:00, 2, 2, 2, 3 <br/>
... <br/>

See `sample_data_small.csv` or `sample_data_large.csv` for detailed examples.

## Usage
### Basic Usage (with default iterations of 1000)
```bash
$python schedule.py input.csv output.csv 
```
### To specify the number of iterations
```bash
$python schedule.py input.csv output.csv --iterations 2000
```
### Constraints Customization
Constraints must be updated in accordance with a input file. Constraint variables can be found in `models.py`.

####Example
```python
MAX_HOURS = 8.25 # targeted hours per worker
MIN_SHIFT_HOURS = 1 # minimum hours of a shift
MAX_SHIFT_HOURS = 4 # maximum hours of a shift
```

## License
MIT
