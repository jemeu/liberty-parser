import tracemalloc


def program():
    x = []
    for i in range(1000000):
        x.append(i)
    return x

def byte_conversion(byte_val):
    for potential_unit in ['B','KB','MB','GB','TB','PB','EB']:
        if byte_val < 1024.000:
            return f"{byte_val:.3f} {potential_unit}"
        else:
            byte_val /= 1024

tracemalloc.start()

program()

current_memory,peak_memory = tracemalloc.get_traced_memory()
print(f"Current memory use: {byte_conversion(current_memory)}")
print(f"Peak memory use: {byte_conversion(peak_memory)}")


tracemalloc.stop()