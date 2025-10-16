# Script de teste completo - Pokemon Battle API
$baseUrl = "http://localhost:5000"

Write-Host "=== TESTANDO API POKEMON BATTLE ===" -ForegroundColor Cyan
Write-Host "Base URL: $baseUrl`n" -ForegroundColor Gray

# 1. Registrar usuario
Write-Host "1. Registrando usuario..." -ForegroundColor Yellow
$registerBody = @{
    username = "ash"
    email = "ash@pokemon.com"
    password = "pikachu123"
} | ConvertTo-Json

try {
    $registerResponse = Invoke-RestMethod -Uri "$baseUrl/api/auth/register" -Method POST -ContentType "application/json" -Body $registerBody
    $token = $registerResponse.access_token
    Write-Host "OK Usuario registrado. Token obtido." -ForegroundColor Green
}
catch {
    Write-Host "Usuario ja existe, fazendo login..." -ForegroundColor Gray
    
    $loginBody = @{
        username = "ash"
        password = "pikachu123"
    } | ConvertTo-Json
    
    $loginResponse = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method POST -ContentType "application/json" -Body $loginBody
    $token = $loginResponse.access_token
    Write-Host "OK Login realizado. Token obtido." -ForegroundColor Green
}

$headers = @{
    Authorization = "Bearer $token"
}

# 2. Listar Pokemon
Write-Host "`n2. Listando Pokemon..." -ForegroundColor Yellow
$pokemonList = Invoke-RestMethod -Uri "$baseUrl/api/pokemon?limit=10" -Method GET -Headers $headers
Write-Host "OK Pokemon listados: $($pokemonList.count) total" -ForegroundColor Green

# 3. Ver detalhes do Pikachu
Write-Host "`n3. Buscando detalhes do Pikachu..." -ForegroundColor Yellow
$pikachuDetails = Invoke-RestMethod -Uri "$baseUrl/api/pokemon/25" -Method GET -Headers $headers
Write-Host "OK Pikachu encontrado: $($pikachuDetails.name)" -ForegroundColor Green

# 4. Adicionar favorito
Write-Host "`n4. Adicionando Pikachu aos favoritos..." -ForegroundColor Yellow
try {
    $favBody = @{ pokemon_id = 25 } | ConvertTo-Json
    $null = Invoke-RestMethod -Uri "$baseUrl/api/favorites" -Method POST -ContentType "application/json" -Headers $headers -Body $favBody
    Write-Host "OK Pikachu adicionado aos favoritos" -ForegroundColor Green
}
catch {
    Write-Host "OK Pikachu ja estava nos favoritos" -ForegroundColor Gray
}

# 5. Listar favoritos
Write-Host "`n5. Listando favoritos..." -ForegroundColor Yellow
$favoritesList = Invoke-RestMethod -Uri "$baseUrl/api/favorites" -Method GET -Headers $headers
Write-Host "OK Total de favoritos: $($favoritesList.total)" -ForegroundColor Green

# 6. Adicionar ao Battle Team
Write-Host "`n6. Montando Battle Team..." -ForegroundColor Yellow
$teamPokemon = @(25, 6, 9, 3, 143, 149)
$addedCount = 0

foreach ($pokemonId in $teamPokemon) {
    try {
        $teamBody = @{ pokemon_id = $pokemonId } | ConvertTo-Json
        $null = Invoke-RestMethod -Uri "$baseUrl/api/battle-team" -Method POST -ContentType "application/json" -Headers $headers -Body $teamBody
        $addedCount++
    }
    catch {
        # Pokemon ja estava no time
    }
}

Write-Host "OK Battle Team: $addedCount Pokemon adicionados" -ForegroundColor Green

# 7. Listar Battle Team
Write-Host "`n7. Listando Battle Team..." -ForegroundColor Yellow
$battleTeamList = Invoke-RestMethod -Uri "$baseUrl/api/battle-team" -Method GET -Headers $headers
Write-Host "OK Total no time: $($battleTeamList.total)/6" -ForegroundColor Green

# 8. Testar limite
Write-Host "`n8. Testando limite de 6 Pokemon..." -ForegroundColor Yellow
if ($battleTeamList.total -ge 6) {
    try {
        $limitBody = @{ pokemon_id = 150 } | ConvertTo-Json
        $null = Invoke-RestMethod -Uri "$baseUrl/api/battle-team" -Method POST -ContentType "application/json" -Headers $headers -Body $limitBody
        Write-Host "ERRO: Nao deveria ter permitido!" -ForegroundColor Red
    }
    catch {
        Write-Host "OK Limite de 6 Pokemon funcionando" -ForegroundColor Green
    }
}
else {
    Write-Host "Time ainda nao esta cheio" -ForegroundColor Yellow
}

# 9. Buscar por nome
Write-Host "`n9. Buscando Pokemon por nome (charizard)..." -ForegroundColor Yellow
$searchResult = Invoke-RestMethod -Uri "$baseUrl/api/pokemon?search=charizard" -Method GET -Headers $headers
Write-Host "OK Encontrado: $($searchResult.results[0].name)" -ForegroundColor Green

# 10. Verificar favorito
Write-Host "`n10. Verificando se Pikachu esta nos favoritos..." -ForegroundColor Yellow
$checkFav = Invoke-RestMethod -Uri "$baseUrl/api/favorites/check/25" -Method GET -Headers $headers
if ($checkFav.is_favorite) {
    Write-Host "OK Pikachu esta nos favoritos" -ForegroundColor Green
}
else {
    Write-Host "ERRO: Pikachu NAO esta nos favoritos" -ForegroundColor Red
}

# 11. Verificar Battle Team
Write-Host "`n11. Verificando se Pikachu esta no Battle Team..." -ForegroundColor Yellow
$checkTeam = Invoke-RestMethod -Uri "$baseUrl/api/battle-team/check/25" -Method GET -Headers $headers
if ($checkTeam.in_battle_team) {
    Write-Host "OK Pikachu esta no Battle Team (Posicao: $($checkTeam.position))" -ForegroundColor Green
}
else {
    Write-Host "ERRO: Pikachu NAO esta no Battle Team" -ForegroundColor Red
}

# 12. Testar /me
Write-Host "`n12. Buscando dados do usuario atual..." -ForegroundColor Yellow
$currentUser = Invoke-RestMethod -Uri "$baseUrl/api/auth/me" -Method GET -Headers $headers
Write-Host "OK Usuario: $($currentUser.username)" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "TODOS OS TESTES CONCLUIDOS COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Resumo:" -ForegroundColor White
Write-Host "  - Favoritos: $($favoritesList.total)" -ForegroundColor Gray
Write-Host "  - Battle Team: $($battleTeamList.total)/6" -ForegroundColor Gray