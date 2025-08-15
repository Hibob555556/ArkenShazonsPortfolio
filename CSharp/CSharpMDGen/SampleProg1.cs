using System;
using System.Collections.Generic;

namespace SampleProject
{
    /// <summary>
    /// Represents a basic task with a name and a status.
    /// </summary>
    public class Task
    {
        /// <summary>
        /// Gets or sets the name of the task.
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Gets or sets whether the task is completed.
        /// </summary>
        public bool IsCompleted { get; set; }

        /// <summary>
        /// Initializes a new instance of the Task class.
        /// </summary>
        /// <param name="name">The name of the task.</param>
        public Task(string name)
        {
            Name = name;
            IsCompleted = false;
        }

        /// <summary>
        /// Marks the task as completed.
        /// </summary>
        public void Complete()
        {
            IsCompleted = true;
        }
    }

    /// <summary>
    /// Manages a list of tasks.
    /// </summary>
    public class TaskManager
    {
        private readonly List<Task> _tasks = new List<Task>();

        /// <summary>
        /// Adds a new task to the manager.
        /// </summary>
        /// <param name="taskName">The name of the task to add.</param>
        public void AddTask(string taskName)
        {
            _tasks.Add(new Task(taskName));
        }

        /// <summary>
        /// Completes the task with the given name.
        /// </summary>
        /// <param name="taskName">The name of the task to complete.</param>
        public void CompleteTask(string taskName)
        {
            var task = _tasks.Find(t => t.Name == taskName);
            if (task != null)
            {
                task.Complete();
            }
        }

        /// <summary>
        /// Displays all tasks and their completion status.
        /// </summary>
        public void DisplayTasks()
        {
            foreach (var task in _tasks)
            {
                Console.WriteLine($"- {task.Name} (Completed: {task.IsCompleted})");
            }
        }
    }

    class Program
    {
        static void Entry(string[] args)
        {
            TaskManager manager = new TaskManager();
            manager.AddTask("Write parser");
            manager.AddTask("Test parser");
            manager.CompleteTask("Write parser");
            manager.DisplayTasks();
        }
    }
}
