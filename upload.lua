wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"

-- Read token from environment variable
local auth_token = os.getenv("SCICAT_ACCESS_TOKEN")
if auth_token then
    wrk.headers["Authorization"] = "Bearer " .. auth_token
else
    print("Warning: SCICAT_ACCESS_TOKEN environment variable is not set.")
end

-- Function to read dataset JSON file
function read_file(file_path)
    local file = io.open(file_path, "r")
    if not file then
        return nil
    end
    local content = file:read("*all")
    file:close()
    return content
end

-- Read the dataset file once
local body = read_file("upload.json")
if not body then
    print("Error: Could not read upload.json")
end

request = function()
    return wrk.format(nil, nil, nil, body)
end

response = function(status, headers, body)
    if status >= 300 then
        print("Response Status: " .. status)
        print("Body: " .. body)
    end
end
