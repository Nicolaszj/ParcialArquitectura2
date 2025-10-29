# Script de Prueba Rápida - PowerShell
# Guarda este archivo como test_api.ps1 y ejecútalo

Write-Host "=== Prueba Rápida de Task API ===" -ForegroundColor Green

# 1. Health Check
Write-Host "`n1. Probando Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✅ Health: $($response.status) - $($response.message)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

# 2. Listar tareas (vacío al inicio)
Write-Host "`n2. Listando tareas..." -ForegroundColor Yellow
try {
    $tasks = Invoke-RestMethod -Uri "http://localhost:8000/tasks" -Method Get
    Write-Host "✅ Tareas encontradas: $($tasks.Count)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

# 3. Crear primera tarea
Write-Host "`n3. Creando primera tarea..." -ForegroundColor Yellow
try {
    $body = @{
        title = "Completar examen de arquitectura"
        status = "pending"
    } | ConvertTo-Json

    $task1 = Invoke-RestMethod -Uri "http://localhost:8000/tasks" `
        -Method Post `
        -Body $body `
        -ContentType "application/json"
    
    Write-Host "✅ Tarea creada:" -ForegroundColor Green
    Write-Host "   ID: $($task1.id)" -ForegroundColor Cyan
    Write-Host "   Título: $($task1.title)" -ForegroundColor Cyan
    Write-Host "   Status: $($task1.status)" -ForegroundColor Cyan
    
    $taskId1 = $task1.id
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

# 4. Crear segunda tarea
Write-Host "`n4. Creando segunda tarea..." -ForegroundColor Yellow
try {
    $body = @{
        title = "Documentar el código"
        status = "done"
    } | ConvertTo-Json

    $task2 = Invoke-RestMethod -Uri "http://localhost:8000/tasks" `
        -Method Post `
        -Body $body `
        -ContentType "application/json"
    
    Write-Host "✅ Tarea creada: $($task2.title) [$($task2.status)]" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

# 5. Listar todas las tareas
Write-Host "`n5. Listando todas las tareas..." -ForegroundColor Yellow
try {
    $tasks = Invoke-RestMethod -Uri "http://localhost:8000/tasks" -Method Get
    Write-Host "✅ Total de tareas: $($tasks.Count)" -ForegroundColor Green
    foreach ($task in $tasks) {
        Write-Host "   - $($task.title) [$($task.status)]" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

# 6. Obtener tarea específica
if ($taskId1) {
    Write-Host "`n6. Obteniendo tarea específica..." -ForegroundColor Yellow
    try {
        $task = Invoke-RestMethod -Uri "http://localhost:8000/tasks/$taskId1" -Method Get
        Write-Host "✅ Tarea encontrada: $($task.title)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
    }

    # 7. Actualizar tarea a 'done'
    Write-Host "`n7. Actualizando tarea a 'done'..." -ForegroundColor Yellow
    try {
        $body = @{
            status = "done"
        } | ConvertTo-Json

        $updated = Invoke-RestMethod -Uri "http://localhost:8000/tasks/$taskId1" `
            -Method Put `
            -Body $body `
            -ContentType "application/json"
        
        Write-Host "✅ Tarea actualizada: $($updated.title) -> $($updated.status)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
    }
}

# 8. Filtrar por status
Write-Host "`n8. Filtrando tareas por status 'done'..." -ForegroundColor Yellow
try {
    $doneTasks = Invoke-RestMethod -Uri "http://localhost:8000/tasks?status=done" -Method Get
    Write-Host "✅ Tareas completadas: $($doneTasks.Count)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

Write-Host "`n=== Pruebas Completadas ===" -ForegroundColor Green
Write-Host "Abre http://localhost:8000/docs para más pruebas interactivas" -ForegroundColor Cyan
