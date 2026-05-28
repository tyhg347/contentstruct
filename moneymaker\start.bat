@echo off
echo ========================================
echo  ContentStruct — MCP + REST API Server
echo ========================================
echo.
echo [1] Start REST API (port 8767)
echo [2] Start MCP Server (stdio - for Claude/Cursor)
echo [3] Start both
echo.
set /p choice="Select (1/2/3): "

if "%choice%"=="1" goto api
if "%choice%"=="2" goto mcp
if "%choice%"=="3" goto both
goto end

:api
echo Starting REST API on http://localhost:8767...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8767 --reload
goto end

:mcp
echo Starting MCP Server (stdio mode)...
echo Connect your MCP client to: python mcp_server/server.py
python mcp_server/server.py
goto end

:both
echo Starting REST API on http://localhost:8767...
start "ContentStruct API" python -m uvicorn app.main:app --host 0.0.0.0 --port 8767
echo Starting MCP Server...
python mcp_server/server.py
goto end

:end
pause
