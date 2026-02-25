#!/usr/bin/env pwsh
# ============================================================
# deploy.ps1 – Windows Deployment Script
# Phase 4: Pulls the latest Docker image and runs the container
# Usage: .\deploy.ps1 [-Registry "registry.gitlab.com/user/repo"] [-Tag "latest"]
# ============================================================

param(
    [string]$Registry = $env:CI_REGISTRY_IMAGE,
    [string]$Tag = "latest",
    [string]$ContainerName = "ecommerce-app",
    [int]$Port = 8000
)

$IMAGE = "${Registry}:${Tag}"

Write-Host "========================================"
Write-Host " Django E-commerce Deployment Script"
Write-Host "========================================"
Write-Host "Image    : $IMAGE"
Write-Host "Container: $ContainerName"
Write-Host "Port     : $Port"
Write-Host "========================================"

# Step 1: Login to GitLab Registry (uses env vars set by CI or manually)
if ($env:CI_REGISTRY_USER -and $env:CI_REGISTRY_PASSWORD -and $env:CI_REGISTRY) {
    Write-Host "`n[1/5] Logging in to GitLab Container Registry..."
    docker login -u $env:CI_REGISTRY_USER -p $env:CI_REGISTRY_PASSWORD $env:CI_REGISTRY
    if ($LASTEXITCODE -ne 0) { Write-Error "Login failed!"; exit 1 }
} else {
    Write-Host "`n[1/5] Skipping registry login (variables not set - using local image)"
}

# Step 2: Pull the latest Docker image
Write-Host "`n[2/5] Pulling latest Docker image..."
docker pull $IMAGE
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Pull failed - will try to use locally built image."
}

# Step 3: Stop and remove existing container
Write-Host "`n[3/5] Stopping existing container '$ContainerName'..."
$existing = docker ps -aq --filter "name=$ContainerName"
if ($existing) {
    docker stop $ContainerName | Out-Null
    docker rm $ContainerName | Out-Null
    Write-Host "  -> Container stopped and removed."
} else {
    Write-Host "  -> No existing container found."
}

# Step 4: Run the new container
Write-Host "`n[4/5] Starting container '$ContainerName' on port $Port..."
docker run -d `
    --name $ContainerName `
    -p "${Port}:8000" `
    --restart unless-stopped `
    $IMAGE

if ($LASTEXITCODE -ne 0) { Write-Error "Failed to start container!"; exit 1 }

# Step 5: Verify container is running
Write-Host "`n[5/5] Verifying deployment..."
Start-Sleep -Seconds 3
$status = docker ps --filter "name=$ContainerName" --format "{{.Status}}"
if ($status) {
    Write-Host "  -> Container status: $status"
    Write-Host ""
    Write-Host "========================================"
    Write-Host "Deployment successful"
    Write-Host "App running at: http://localhost:$Port"
    Write-Host "========================================"
} else {
    Write-Error "Container is not running! Check logs: docker logs $ContainerName"
    exit 1
}
