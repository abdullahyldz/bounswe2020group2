package com.example.getflix.ui.adapters

import android.graphics.Paint
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.navigation.findNavController
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.getflix.R
import com.example.getflix.activities.MainActivity
import com.example.getflix.addToShoppingCart
import com.example.getflix.databinding.CardHomeRecommendedProductBinding
import com.example.getflix.databinding.CardVendorProductBinding
import com.example.getflix.models.ProductModel
import com.example.getflix.ui.fragments.CartFragmentDirections
import com.example.getflix.ui.fragments.NByTwoGridFragmentDirections
import com.example.getflix.ui.fragments.NByTwoGridFragmentDirections.Companion.actionNByTwoGridFragmentToProductFragment
import com.example.getflix.ui.fragments.VendorPageFragmentDirections
import com.example.getflix.ui.viewmodels.HomeViewModel
import com.squareup.picasso.Picasso

class VendorPageProductAdapter(var fragment: Fragment) :
    ListAdapter<ProductModel, VendorPageProductAdapter.ViewHolder>(VendorProductDiffCallback()) {



    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = getItem(position)
        holder.bind(item)
        holder?.itemView!!.setOnClickListener {
            fragment.view?.findNavController()
                ?.navigate(VendorPageFragmentDirections.actionVendorFragmentToProductFragment(
                        item.id
                    )
                )
        }
    }

    private fun ViewHolder.bind(product: ProductModel) {
        if(product.images[0].contains("/image/"))
            Picasso.get().load("http://3.134.80.26:8000" + product.images[0]).into(binding.productImage)
        else
            Picasso.get().load(product.images[0]).into(binding.productImage)

        var amount = binding.amountRecProduct.text.toString().toInt()

        binding.product = product

        if(product.name.length>70) {
            binding.productName.text = product.name.substring(0, 70)
        } else {
            binding.productName.text = product.name
        }
        if (product.price.toString().length > 5) {
            binding.oldProductPrice.text = product.price.toString().substring(0, 5) + " TL"
        } else {
            binding.oldProductPrice.text = product.price.toString() + " TL"

        }

        binding.oldProductPrice.setPaintFlags(binding.oldProductPrice.getPaintFlags() or Paint.STRIKE_THRU_TEXT_FLAG)
        if (product.priceDiscounted.toString().length > 5) {
            binding.productPrice.text =
                product.priceDiscounted.toString().substring(0, 5) + " TL"

        } else {
            binding.productPrice.text = product.priceDiscounted.toString() + " TL"

        }
        if (MainActivity.StaticData.isCustomer) {
            binding.addShopping.setOnClickListener {
                addToShoppingCart(amount, 1, product.id)
            }
        }
        binding.decreaseRecProduct.setOnClickListener {
            if (amount > 1) {
                amount = amount.dec()
                binding.amountRecProduct.text = amount.toString()
            }
        }
        binding.increaseRecProduct.setOnClickListener {
            amount = amount.inc()
            binding.amountRecProduct.text = amount.toString()

        }
        binding.save.setOnClickListener {
                //binding.save.setImageResource(R.drawable.saved_product)
                //binding.save.setImageResource(R.drawable.nonsaved_product)
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        return ViewHolder.from(parent)
    }

    class ViewHolder private constructor(val binding: CardVendorProductBinding) :
        RecyclerView.ViewHolder(binding.root) {
        companion object {
            fun from(parent: ViewGroup): ViewHolder {
                val layoutInflater = LayoutInflater.from(parent.context)
                val binding =
                    CardVendorProductBinding.inflate(layoutInflater, parent, false)
                return ViewHolder(binding)
            }
        }

    }
}

class VendorProductDiffCallback : DiffUtil.ItemCallback<ProductModel>() {
    override fun areItemsTheSame(oldItem: ProductModel, newItem: ProductModel): Boolean {
        return oldItem === newItem
    }

    override fun areContentsTheSame(oldItem: ProductModel, newItem: ProductModel): Boolean {
        return oldItem == newItem
    }

}

