from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserRegistrationForm, UserProfileForm, AddressForm
from .models import Address


def register(request):
    """Inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès!')
            return redirect('shop:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """Connexion utilisateur"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.username}!')
            next_url = request.GET.get('next', 'shop:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'accounts/login.html')


def user_logout(request):
    """Déconnexion utilisateur"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('shop:home')


@login_required
def profile(request):
    """Profil utilisateur"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            # Mettre à jour aussi les informations de base de l'utilisateur
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
            messages.success(request, 'Votre profil a été mis à jour!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def change_password(request):
    """Changement de mot de passe"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été changé avec succès!')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def address_list(request):
    """Liste des adresses de l'utilisateur"""
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/address_list.html', {'addresses': addresses})


@login_required
def address_create(request):
    """Créer une nouvelle adresse"""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Adresse ajoutée avec succès!')
            return redirect('accounts:address_list')
    else:
        form = AddressForm()
    
    return render(request, 'accounts/address_form.html', {'form': form, 'action': 'Ajouter'})


@login_required
def address_edit(request, pk):
    """Modifier une adresse existante"""
    address = get_object_or_404(Address, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Adresse modifiée avec succès!')
            return redirect('accounts:address_list')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'accounts/address_form.html', {'form': form, 'action': 'Modifier'})


@login_required
def address_delete(request, pk):
    """Supprimer une adresse"""
    address = get_object_or_404(Address, pk=pk, user=request.user)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Adresse supprimée avec succès!')
        return redirect('accounts:address_list')
    
    return render(request, 'accounts/address_confirm_delete.html', {'address': address})
