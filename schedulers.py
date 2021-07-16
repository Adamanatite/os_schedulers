from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates

class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        """Chooses the first event in the queue to execute

        Parameters:
        cur_event (Event): The last event in the simulation

        Returns:
        Process: The process to be executed next
        """
        #Choose first ready process in list
        for process in self.processes:
            if process.process_state is ProcessStates.READY:
                return process

    def dispatcher_func(self, cur_process):
        """Executes the given process to completion

        Parameters:
        cur_process (Process): The process to be executed

        Returns:
        Event: The event generated from this execution
        """
        #Run process to completion and increment time
        cur_process.process_state = ProcessStates.RUNNING
        newTime = self.time + cur_process.run_for(cur_process.service_time, self.time)
        #Terminate process and return event
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id = cur_process.process_id, event_type = EventTypes.PROC_CPU_DONE, event_time = newTime)

class SJF(SchedulerDES):

    def scheduler_func(self, cur_event):
        """Chooses the shortest event in the queue to execute

        Parameters:
        cur_event (Event): The last event in the simulation

        Returns:
        Process: The process to be executed next
        """
        #Sort processes from shortest to longest service time
        sortedProcesses = sorted(self.processes,
        key = lambda p: p.service_time)
        #Find first ready process and choose it
        for process in sortedProcesses:
            if process.process_state is ProcessStates.READY:
                return process

    def dispatcher_func(self, cur_process):
        """Executes the given process to completion

        Parameters:
        cur_process (Process): The process to be executed

        Returns:
        Event: The event generated from this execution
        """
        #Run process to completion and increment time
        cur_process.process_state = ProcessStates.RUNNING
        newTime = self.time + cur_process.run_for(cur_process.service_time, self.time)
        #Terminate process and return event
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id = cur_process.process_id, event_type = EventTypes.PROC_CPU_DONE, event_time = newTime)


class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        """Executes the first process in the queue for a quantum and moves it to the back of the queue

        Parameters:
        cur_event (Event): The last event in the simulation

        Returns:
        Process: The process to be executed next
        """
        #Save the id of the event process
        id = cur_event.process_id
        #Get the process which requested cpu time
        for process in self.processes:
            if process.process_id == id:
                #Move process to end of queue
                self.processes.remove(process)
                self.processes.append(process)
                return process

    def dispatcher_func(self, cur_process):
        """Executes the given process for the time quantum

        Parameters:
        cur_process (Process): The process to be executed

        Returns:
        Event: The event generated from this execution
        """
        #Set to running
        cur_process.process_state = ProcessStates.RUNNING
        #Run process for the time quantum
        newTime = self.time + cur_process.run_for(self.quantum, self.time)
        #Set event type and process state based on completion
        if cur_process.remaining_time == 0:
            type = EventTypes.PROC_CPU_DONE
            cur_process.process_state = ProcessStates.TERMINATED
        else:
            type = EventTypes.PROC_CPU_REQ
            cur_process.process_state = ProcessStates.READY
        #Return event
        return Event(process_id = cur_process.process_id, event_type = type, event_time = newTime)


class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        """Chooses the process with shortest remaining time to execute

        Parameters:
        cur_event (Event): The last event in the simulation

        Returns:
        Process: The process to be executed next
        """
        #Sort processes from shortest to longest remaining time
        self.processes.sort(key = lambda p: p.remaining_time)
        #Find first ready process and choose it
        for process in self.processes:
            if process.process_state is ProcessStates.READY:
                return process

    def dispatcher_func(self, cur_process):
        """Executes the given process for a cpu burst or until pre-empted

        Parameters:
        cur_process (Process): The process to be executed

        Returns:
        Event: The event generated from this execution
        """
        #Set to running
        cur_process.process_state = ProcessStates.RUNNING
        #Run process until next event
        newTime = self.time + cur_process.run_for(self.next_event_time() - self.time, self.time)
        #Set event type and process state based on completion
        if cur_process.remaining_time <= 0:
            type = EventTypes.PROC_CPU_DONE
            cur_process.process_state = ProcessStates.TERMINATED
        else:
            type = EventTypes.PROC_CPU_REQ
            cur_process.process_state = ProcessStates.READY
        #Return event
        return Event(process_id = cur_process.process_id, event_type = type, event_time = newTime)
