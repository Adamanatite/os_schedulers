# os_schedulers
Python code to represent the behaviour of various OS schedulers

# Schedulers:
  * <b>FCFS (First Come First Served):</b> Executes the first process in the queue until completion (Non-preemptive)
  * <b>SJF (Shortest Job First):</b> Executes the shortest process in the queue until completion (Non-preemptive)
  * <b>RR (Round Robin):</b> Executes each process in the queue for a given quantum and moves it to the back of the queue (Preemptive)
  * <b>SRTF (Shortest Remaining Time First):</b> Executes the process with the current least time remaining until completion (Preemptive)
