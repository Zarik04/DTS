import multiprocessing

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.Rv = 0  # Number of virtual instances
        self.Ri = 0  # Number of actual instances
        self.tTF = float('inf')  # Temporary finish time
        self.parents = []
        self.children = []

class Processor:
    def __init__(self, processor_id, computation_speed):
        self.processor_id = processor_id
        self.computation_speed = computation_speed
        self.tEA = 0  # Estimated available time

class Scheduler:
    def __init__(self, nodes, processors, Rmax):
        self.nodes = nodes
        self.processors = processors
        self.Rmax = Rmax
        self.SR = []  # Set of ready nodes

    def compute_ranks(self):
        # Implement rank computation logic here
        pass

    def select_ready_node(self):
        return self.SR.pop(0)

    def select_idle_processor(self):
        for node in self.SR:
            if node.Ri < self.Rmax:
                return node
        return None

    def update_computation_speed_and_available_time(self, processor_id, computation_speed, available_time):
        processor = self.processors[processor_id]
        processor.computation_speed = computation_speed
        processor.tEA = available_time

    def execute_node(self, node, processor):
        # Implement the execution logic for a node on a processor
        pass

    def process_node(self, selected_node, selected_processor):
        # Execute the node on the processor
        self.execute_node(selected_node, selected_processor)

        # Update Ri and Rv
        selected_node.Ri += 1
        selected_node.Rv += 1

        # Update tTF if necessary
        if selected_node.tTF > selected_processor.tEA:
            selected_node.tTF = selected_processor.tEA

        # Update the children's ready state
        for child in selected_node.children:
            child.parents.remove(selected_node)
            if not child.parents:
                self.SR.append(child)

    def schedule_tasks(self):
        while True:
            unfinished_nodes_exist = any(node.tTF != float('inf') for node in self.nodes)

            if not unfinished_nodes_exist:
                break

            # Update Rv and tTF for nodes in SR
            for node in self.SR:
                node.Rv = node.Ri
                node.tTF = float('inf')

            # Update tTA for each processor
            for processor in self.processors:
                tTAk = max(node.tTF for node in self.SR) if self.SR else 0
                processor.tEA = tTAk

            # Process nodes using idle processors
            while True:
                selected_node = None
                selected_processor = None

                # Find an idle processor and unfinished node with Ri < Rmax
                for node in self.SR:
                    if node.Ri < self.Rmax:
                        selected_node = node
                        break

                if selected_node is None:
                    break

                if selected_node.Ri < self.Rmax:
                    selected_processor = self.select_idle_processor()

                if selected_processor is None:
                    break

                self.process_node(selected_node, selected_processor)

        # Main program
        # Create nodes
        nodes = []
        for i in range(M):
            nodes.append(Node(i))

        # Create processors
        processors = []
        for i in range(K):
            processors.append(Processor(i, Ck[i]))

        # Create scheduler
        scheduler = Scheduler(nodes, processors, Rmax)

        # Compute ranks
        scheduler.compute_ranks()

        # Start scheduling tasks
        scheduler.schedule_tasks()
