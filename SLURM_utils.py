class SLURM_settings:
    def __init__(self, job_name=None, email=None, partition=None, time=None, 
                 cpus=None, mem=None, gpus=None, nodes=None, account=None, 
                 logdir=None, array=None, mail_type=None, header="#!/bin/bash"):
        self.header = header
        self.job_name = job_name
        self.email = email
        self.partition = partition
        self.time = time
        self.cpus = cpus
        self.mem = mem
        self.gpus = gpus
        self.nodes = nodes
        self.account = account
        self.logdir = logdir
        self.array = array
        self.mail_type = mail_type
    def basic(self):
        self.job_name = ' '
        self.email = ' '
        self.partition = 'standard'
        self.time = '01:00:00'
        self.cpus = 1
        self.mem = '5g'
        self.account= ' '
        self.logdir = ' '
    def write_settings(self, filename):
        
        with open(filename, 'w') as f:
            f.write(f'{self.header}\n\n')
            f.write(f'#SBATCH --job-name={self.job_name}\n')
            f.write(f'#SBATCH --mail-type={self.mail_type}\n')
            f.write(f'#SBATCH --mail-user={self.email}\n')
            f.write(f'#SBATCH --partition={self.partition}\n')
            f.write(f'#SBATCH --time={self.time}\n')
            f.write(f'#SBATCH --account={self.account}\n')
            f.write(f'#SBATCH --output={self.logdir}/{self.job_name}.log\n')
            if self.array != None: f.write(f'#SBATCH --array={self.array}\n')
            if self.nodes != None: f.write(f'#SBATCH --nodes={self.nodes}\n')
            if self.gpus == None:
                f.write(f'#SBATCH --cpus-per-task={self.cpus}\n')
                f.write(f'#SBATCH --mem-per-cpu={self.mem}\n')
            else:
                f.write(f'#SBATCH --gpus-per-task={self.gpus}\n')
                f.write(f'#SBATCH --gres=gpu:{self.gpus}\n')
                f.write(f'#SBATCH --mem-per-gpu={self.mem}\n')
                f.write(f'#SBATCH --cpus-per-task={self.cpus}\n')
#     def import_settings(self, settings):
#         if settings in profiles:
#             self
# profiles = ['gpu', 'cpu', 'GALD', 'MD']

GALD_HT = SLURM_settings(
    job_name = 'GALD',
    email = 'riverseb@umich.edu',
    partition = 'standard',
    time = '01:00:00',
    cpus = 1,
    mem = '5g',
    account = 'maom99',
    logdir = ' ',
    array = "1-100",
    mail_type = 'BEGIN,END,FAIL'
)
