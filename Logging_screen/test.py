#%%
import logging  # Import the actual logging module
level = "INFO"
log_function = getattr(logging, level.lower(), None)
print(log_function)
# %%
