# WooCommerce Shop — Setup Guide (Whatshername.uk)

The kit ships a **Shop page** (`templates/shop.json`) styled to match the
minimalist look — framed artwork, price, and an *Add to Cart* button. Right now
those cards are a **static scaffold**: they show the layout but don't actually
take money. This guide turns them into a real shop that sells **original
paintings** and **limited prints**, with a cart, checkout and payments.

Everything below is done in WordPress admin. Budget ~1–2 hours the first time.

---

## 1. Install WooCommerce

1. **Plugins → Add New**, search **WooCommerce**, **Install → Activate**.
2. Run its setup wizard:
   - **Store address**: your UK address (used for tax/shipping).
   - **Currency**: GBP (£).
   - **Selling**: Physical products.
   - Skip the marketing/upsell add-ons for now.
3. WooCommerce creates 4 pages automatically: **Shop, Cart, Checkout, My
   Account**. You'll point the design at these in step 5.

> Keep Elementor Pro active — it has WooCommerce Builder widgets that make the
> product pages match this theme.

---

## 2. Store settings that matter for art

**WooCommerce → Settings:**

- **General** → selling location UK + wherever you'll ship; enable taxes only if
  you're VAT-registered (most emerging artists aren't — leave off until you are).
- **Products → Inventory** → tick **Enable stock management**. Originals are
  **1 of 1**, so this stops two people buying the same canvas.
- **Shipping** → create **Shipping Zones**:
  - *UK* → flat rate (e.g. £8 small print / £25 large original, or free over £X).
  - *Europe / International* → higher flat rates, or "local pickup" for
    originals you'd rather hand over / arrange couriers for.
  - Consider a **"Collection in person / arrange courier"** method for large
    originals so you're not locked into a postage price.

---

## 3. Payments

**WooCommerce → Settings → Payments.** Two easy, trusted options:

- **Stripe** (cards, Apple/Google Pay) — install *WooCommerce Stripe Gateway*,
  connect your Stripe account.
- **PayPal Payments** — install *WooCommerce PayPal Payments*, connect PayPal.

Enable one or both. Test with Stripe's test mode before going live.

---

## 4. Add the artwork as Products

**Products → Add New** for each piece:

- **Title**: the painting's name (e.g. *Love, Always*).
- **Description**: story, inspiration, what's included (certificate, signature).
- **Product image** + **gallery**: the real photos (studio shot + detail shots).
- **Categories** (right sidebar): create **Originals** and **Prints** (and maybe
  *Hearts*, *Characters* as tags).

Then set it up by type:

### Original paintings (one of a kind)
- **Product data → Simple product**.
- Set the **Regular price** (e.g. 1200).
- **Inventory** tab → **Manage stock** → **Stock quantity: 1**. When it sells,
  Woo marks it *Sold out* automatically.
- **Shipping** tab → weight/dimensions so shipping rates calculate.

### Prints (limited editions, multiple sizes)
- **Product data → Variable product**.
- **Attributes** tab → add an attribute **Size** (A4 | A3 | A2), tick *Used for
  variations*.
- **Variations** tab → generate from attributes, set a price per size and a
  stock number per size (e.g. edition of 25).

Publish each. They'll appear in the shop automatically.

---

## 5. Make the shop match this theme (Elementor Pro)

You have two clean options:

### Option A — quickest
Use the **static `shop.json` page** as your landing/lookbook, and let each
"Add to Cart" / "View" link point to the **real WooCommerce product**. Good if
you have a handful of pieces and like hand-curating the layout.

### Option B — fully automatic (recommended once you have >6 pieces)
Rebuild the shop with Woo's dynamic widgets so new products appear on their own:

1. Edit the **Shop** page in Elementor.
2. Delete the static product columns.
3. Drop in the **Products** widget (search "Products" in the widget panel) →
   it lists real products in a grid. Set **Columns: 3**, and under **Style** set:
   - Title font **Special Elite**, colour `#2B2B2B`
   - Price colour `#BF3B34`
   - Button: background `#2B2B2B`, text uppercase **Courier Prime**
4. (Optional) Add the **Product Categories** widget above it as the filter row.

### Single Product template (so every product page matches)
1. **Templates → Theme Builder → Single Product → Add New**.
2. Build with Woo widgets: **Product Images**, **Product Title** (Special Elite),
   **Product Price** (`#BF3B34`), **Add to Cart**, **Short Description**,
   **Product Data Tabs**.
3. Wrap the image in the same framed look: a container with a 1px `#E0E0E0`
   border, 14px padding, white background, soft shadow.
4. **Publish → Display Conditions → All Products**.

Style the **Cart**, **Checkout** and **My Account** pages via **Site Settings →
WooCommerce** (or Theme Builder templates) so they inherit the fonts/colours.

---

## 6. Before you go live — checklist

- [ ] One test order end-to-end in Stripe/PayPal **test mode**, then switch live.
- [ ] Originals set to **stock = 1**; prints have per-size stock.
- [ ] Shipping zones cover everywhere you'll actually post to.
- [ ] Order-confirmation emails have your logo/brand (WooCommerce → Settings →
      Emails).
- [ ] **Terms**, **Refund/Returns**, and **Privacy** pages linked at checkout
      (art is often sold as *final sale* — state that clearly).
- [ ] A **packing plan** for originals (tube vs flat vs crated) so postage
      prices are realistic.

---

## 7. Nice-to-haves later

- **Made-to-order / commissions** as a product with a deposit + a form.
- **Wishlist** plugin so buyers can save pieces.
- **Local pickup** + **"enquire about this piece"** button for high-value
  originals (some buyers prefer to talk first).
- **Google/Meta product feed** if you want to advertise.

---

When you're ready, send me a note (or a screenshot of your Products list) and I
can build the **dynamic Products shop page** and the **Single Product Theme
Builder template** in this exact minimalist style and hand them over as importable
JSON — same as the rest of the kit.
