import win32job
import win32api

def limit_memory_windows(max_mem_mb: int):
    """Limit the process to use a maximum of `max_mem_mb` MB (Windows only)."""
    job = win32job.CreateJobObject(None, "")
    info = win32job.QueryInformationJobObject(job, win32job.JobObjectExtendedLimitInformation)

    # Set the memory limit
    max_mem_bytes = max_mem_mb * 1024 * 1024
    info['ProcessMemoryLimit'] = max_mem_bytes
    info['JobMemoryLimit'] = max_mem_bytes
    info['BasicLimitInformation']['LimitFlags'] = (
        win32job.JOB_OBJECT_LIMIT_PROCESS_MEMORY | win32job.JOB_OBJECT_LIMIT_JOB_MEMORY
    )

    win32job.SetInformationJobObject(job, win32job.JobObjectExtendedLimitInformation, info)
    win32job.AssignProcessToJobObject(job, win32api.GetCurrentProcess())