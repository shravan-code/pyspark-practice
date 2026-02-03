**Apache Spark** is a distributed, in-memory data processing engine that breaks an application 
into **jobs**, **stages**, and **tasks**, executes those tasks in parallel across a cluster on data partitions, 
and returns the final result to the user through the **Driver**.

# Driver (Brain of Spark)

The Spark Driver orchestrates execution by creating the SparkContext, building DAGs,
scheduling jobs and tasks, and coordinating with the cluster manager to run tasks on executors.

In Spark, the Driver creates the logical plan using the Catalyst Analyzer, 
optimizes it using the Catalyst Optimizer, and generates the physical execution plan, 
all within the JVM Driver before scheduling execution.

* The Driver creates the SparkContext and SparkSession in the JVM.
* Python code interacts with these JVM objects through Py4J using Python proxy objects.
* The Driver builds an unresolved logical plan, which is resolved by the **Catalyst Analyzer**, 
optimized by the **Catalyst Optimizer**, and converted into a physical plan by the **Physical Planner**.
* Using the physical plan, the Driver constructs a **DAG** representing the computation.
* The Driver owns the DAG Scheduler, which schedules jobs triggered by actions using the DAG.
* Each job is divided into stages at shuffle boundaries.
* Stages are broken into tasks, which are scheduled by the Task Scheduler.
* The Driver requests executors from the Cluster Manager.
* The number of jobs depends on actions, while the number of tasks depends on data partitions.
* Worker nodes are physical or virtual machines that host executors.
* The Cluster Manager manages resources and launches executors on worker nodes.
* Executors run tasks in parallel on partitions and perform the actual computation.
* Results are sent back to the Driver.


![img.png](images/pyspark.webp)
