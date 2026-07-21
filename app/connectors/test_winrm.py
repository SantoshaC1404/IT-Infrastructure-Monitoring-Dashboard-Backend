import winrm

session = winrm.Session(
    "http://192.168.6.119:5985/wsman",
    auth=("bel", "bel@123"),
    transport="ntlm",
)

result = session.run_cmd("hostname")

print(result.status_code)
print(result.std_out.decode())
print(result.std_err.decode())