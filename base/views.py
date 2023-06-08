from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import GameUploadForm, TransactionCheckForm
from .models import Game
from base.scripts_for_ipfs import create_metadata
from base.scripts_for_contract import connect_to_contract
from base.helpful_scripts.interaction_with_transactions import *
from json import dumps, loads


def add_new_game(
    name,
    genre,
    description,
    platform,
    poster,
    images,
    price,
    token_id,
    private_key,
    wallet_address,
):
    new_game = Game.objects.create(
        name=name,
        genre=genre,
        description=description,
        platform=platform,
        poster=poster,
        images=images,
        price=price,
        token_id=token_id,
        private_key=private_key,
        slug=str(name).lower().replace(" ", "_"),
        wallet_address=wallet_address,
    )
    new_game.save()


def main_page(request):
    return render(request, "main_page.html")


def game_uploading(request):
    if request.method == "POST":
        form = GameUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]
            genre = form.cleaned_data["genre"]
            description = form.cleaned_data["description"]
            platform = form.cleaned_data["platform"]
            poster = form.cleaned_data["poster"]
            images = request.FILES.getlist("images")
            game_file = form.cleaned_data["game_file"]
            price = form.cleaned_data["price"]
            wallet_address = form.cleaned_data["wallet_address"]

            (
                game_file_uri,
                encrypted_message,
                key,
            ) = create_metadata.convert_game_file_to_metadata(game_file)
            # u should write real address here, owerwise there will be an error
            wallet_address = "0x99bc949975C4bd87D2a6d2a5043112C121EC68D1"

            # sometimes u have to wait, because it takes time to load into blockchain, that's why sometimes token_id will be wrong
            customer_contract = connect_to_contract.return_contract("Customer")
            game_id = 15
            token_id = customer_contract.create_customer_nft(game_id, wallet_address)

            print(f"token id = {token_id}")

            # token_id = 0
            info = customer_contract.get_gameId_from_tokenId(token_id - 1)

            print(f"info = {info}")

            # developer_contract = connect_to_contract.return_contract("Developer")

            # # sometimes u have to wait, because it takes time to load into blockchain, that's why sometimes token_id will be wrong
            # token_id = developer_contract.create_developer_nft(
            #     encrypted_message, wallet_address
            # )

            # # example how use buy_game contract
            # buy_game_contract = connect_to_contract.return_contract("BuyGame")
            # eth_amount = 10000000000000000  # = 0.01 eth
            # info = buy_game_contract.get_metadata_from_contract(
            #     eth_amount,
            #     "0xc1275DF70ef313C86C5Ac60De81Af1AA9f1F71De",
            #     1,
            #     "0x99bc949975C4bd87D2a6d2a5043112C121EC68D1",
            # )
            # print("Retrieved information:", info)

            poster_uri, images_uri = create_metadata.create_metadata_json(
                poster, images
            )
            add_new_game(
                name,
                genre,
                description,
                platform,
                poster_uri,
                images_uri,
                price,
                token_id,
                key,
                wallet_address,
            )

            return render(request, "main_page.html")
    else:
        form = GameUploadForm()

    return render(request, "game_uploading.html", {"form": form})


def game_catalog(request):
    context = {"games": Game.objects.all()}
    return render(request, "catalog/game_catalog.html", context)


def game_detail(request, slug):
    game = Game.objects.get(slug__iexact=slug)
    images = loads(game.images)

    if request.method == "POST":
        form = TransactionCheckForm(request.POST, request.FILES)
        if form.is_valid():
            transaction_address = form.cleaned_data["transaction_address"]
            developer_wallet = game.wallet_address
            game_price = game.price

            validity, message = check_validity_of_transaction(
                transaction_address, developer_wallet, game_price
            )

            messages.info(request, message)

        return HttpResponseRedirect(game.get_absolute_url())
    else:
        form = TransactionCheckForm()

    return render(
        request,
        "catalog/game_detail.html",
        context={"game": game, "images": images, "form": form},
    )

def about_us(request):
    return render(request, "about_us.html")
