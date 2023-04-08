from criticalpath import Node
p = Node('project')
U=p.add(Node('Start', duration=0))
V=p.add(Node('Sink', duration=0))
a = p.add(Node('p51', duration=1))
b = p.add(Node('p11', duration=1, lag=0))
c = p.add(Node('p81', duration=1, lag=0))
d = p.add(Node('p41', duration=3, lag=0))
e = p.add(Node('p61', duration=1, lag=0))

f = p.add(Node('p52', duration=1, lag=0))
g =p.add(Node('p12', duration=2, lag=0))
h =p.add(Node('p102', duration=2, lag=0))
i =p.add(Node('p72', duration=1, lag=0))
j =p.add(Node('p62', duration=1, lag=0))

k =p.add(Node('p54', duration=1, lag=0))
l =p.add(Node('p14', duration=3, lag=0))
m=p.add(Node('p44', duration=1, lag=0))
n=p.add(Node('p64', duration=1, lag=0))
o=p.add(Node('p74', duration=1, lag=0))

q=p.add(Node('p53',duration =2 ,lag =0))
r=p.add(Node('p93',duration =3 ,lag =0))
s=p.add(Node('p33',duration =3 ,lag =0))
t=p.add(Node('p63',duration =1 ,lag =0))
w=p.add(Node('p73',duration =1 ,lag =0))

x=p.add(Node('p55',duration =3 ,lag =0))
aa=p.add(Node('p25',duration =2 ,lag =0))
ab=p.add(Node('p35',duration =3 ,lag =0))
ac=p.add(Node('p15',duration =3 ,lag =0))
ad=p.add(Node('p75',duration =1 ,lag =0))

ae=p.add(Node('p56',duration =1 ,lag =0))
af=p.add(Node('p26',duration =3 ,lag =0))
ag=p.add(Node('p96',duration =3 ,lag =0))
ah=p.add(Node('p66',duration =3 ,lag =0))
ai=p.add(Node('p76',duration =3 ,lag =0))

aj=p.add(Node('p57',duration =1 ,lag =0))
ak=p.add(Node('p97',duration =2 ,lag =0))
al=p.add(Node('p47',duration =3 ,lag =0))
am=p.add(Node('p17',duration =3 ,lag =0))
an=p.add(Node('p77',duration =2 ,lag =0))

ao=p.add(Node('p59',duration =1 ,lag =0))
ap=p.add(Node('p19',duration =2 ,lag =0))
aq=p.add(Node('p39',duration =3 ,lag =0))
ar=p.add(Node('p69',duration =1 ,lag =0))

au=p.add(Node('p510',duration =1 ,lag =0))
av=p.add(Node('p110',duration =1,lag =0))
aw=p.add(Node('p910',duration =3 ,lag =0))
ax= p.add(Node('p610',duration =2 ,lag =0))

ay=p.add(Node('p58',duration =1 ,lag =0))
az=p.add(Node('p28',duration =3 ,lag =0))
ba=p.add(Node('p48',duration =2 ,lag =0))
bc=p.add(Node('p68',duration =1 ,lag =0))
dd=p.add(Node('p78',duration =3 ,lag =0))

de=p.add(Node('p511',duration =2 ,lag =0))
df=p.add(Node('p111',duration =3,lag =0))
dg=p.add(Node('p711',duration =2 ,lag =0))
dh=p.add(Node('p611',duration =2 ,lag =0))

di=p.add(Node('p512',duration =1 ,lag =0))
dj=p.add(Node('p1012',duration =2,lag =0))
dk=p.add(Node('p312',duration =1 ,lag =0))
dl=p.add(Node('p612',duration =2 ,lag =0))

dm=p.add(Node('p513',duration =3 ,lag =0))
dn=p.add(Node('p213',duration =1,lag =0))
do=p.add(Node('p413',duration =1 ,lag =0))
dp=p.add(Node('p613',duration =1 ,lag =0))

dq=p.add(Node('p514',duration =1 ,lag =0))
dr=p.add(Node('p114',duration =3,lag =0))
ds=p.add(Node('p1014',duration =3 ,lag =0))
dt=p.add(Node('p714',duration =3 ,lag =0))

p.add(Node('p515',duration =1 ,lag =0))
p.add(Node('p915',duration =2,lag =0))
p.add(Node('p415',duration =3 ,lag =0))
p.add(Node('p715',duration =3 ,lag =0))

p.add(Node('p516',duration =2 ,lag =0))
p.add(Node('p216',duration =3,lag =0))
p.add(Node('p816',duration =2 ,lag =0))
p.add(Node('p616',duration =2 ,lag =0))

p.link(a, b).link(b, c).link(c, d).link(d, e).link(a,U).link(e,V)
p.link()
p.update_all()
pathCP=p.get_critical_path()
print(p.duration)

import collections
from ortools.sat.python import cp_model

jobs_data = [  # task = (machine_id, processing_time).
    [(0, 3), (1, 2), (2, 2)],  # Job0
    [(0, 2), (2, 1), (1, 4)],  # Job1
    [(1, 4), (2, 3)]  # Job2
]

machines_count = 1 + max(task[0] for job in jobs_data for task in job)
all_machines = range(machines_count)
# Computes horizon dynamically as the sum of all durations.
horizon = sum(task[1] for job in jobs_data for task in job)
model = cp_model.CpModel()

# Named tuple to store information about created variables.
task_type = collections.namedtuple('task_type', 'start end interval')
# Named tuple to manipulate solution information.
assigned_task_type = collections.namedtuple('assigned_task_type',
                                            'start job index duration')

# Creates job intervals and add to the corresponding machine lists.
all_tasks = {}
machine_to_intervals = collections.defaultdict(list)

for job_id, job in enumerate(jobs_data):
    for task_id, task in enumerate(job):
        machine = task[0]
        duration = task[1]
        suffix = '_%i_%i' % (job_id, task_id)
        start_var = model.NewIntVar(0, horizon, 'start' + suffix)
        end_var = model.NewIntVar(0, horizon, 'end' + suffix)
        interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                            'interval' + suffix)
        all_tasks[job_id, task_id] = task_type(start=start_var,
                                               end=end_var,
                                               interval=interval_var)
        machine_to_intervals[machine].append(interval_var)
# Create and add disjunctive constraints.
for machine in all_machines:
    model.AddNoOverlap(machine_to_intervals[machine])

# Precedences inside a job.
for job_id, job in enumerate(jobs_data):
    for task_id in range(len(job) - 1):
        model.Add(all_tasks[job_id, task_id +
                            1].start >= all_tasks[job_id, task_id].end)