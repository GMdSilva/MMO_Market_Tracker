import pandas as pd


def analyze_price_history(item_name, offer_type, folder_name):
    df = pd.read_csv(f'results/{folder_name}/{item_name}/{offer_type}_base.csv')

    unique_scans = sorted(df['scan'].unique())

    # Initialize lists to store changes
    all_quantity_changes = []
    all_disappeared_offers = []
    all_new_offers = []
    all_disappeared_offer_positions = []
    all_new_offer_prices = []
    offer_residency_times = {}

    # Iterate over each scan
    for i in range(1, len(unique_scans)):
        prev_scan_val = unique_scans[i - 1]
        curr_scan_val = unique_scans[i]

        prev_scan = df[df['scan'] == prev_scan_val]
        curr_scan = df[df['scan'] == curr_scan_val]

        # Detect changes in quantity
        quantity_changes = curr_scan[curr_scan.apply(
            lambda row: any((prev_scan['offer_id'] == row['offer_id']) & (prev_scan['quantity'] != row['quantity'])),
            axis=1)]
        if not quantity_changes.empty:
            quantity_changes['delta_quantity'] = quantity_changes.apply(
                lambda row: row['quantity'] - prev_scan[prev_scan['offer_id'] == row['offer_id']]['quantity'].values[0],
                axis=1)
        all_quantity_changes.append(quantity_changes)

        # Detect disappeared offers
        disappeared_offers = prev_scan[~prev_scan['offer_id'].isin(curr_scan['offer_id'])]
        all_disappeared_offers.append(disappeared_offers)

        # Detect new offers
        new_offers = curr_scan[~curr_scan['offer_id'].isin(prev_scan['offer_id'])]
        all_new_offers.append(new_offers)

        # Track residency time for each offer
        for _, row in prev_scan.iterrows():
            offer_id = row['offer_id']
            if offer_id not in offer_residency_times:
                offer_residency_times[offer_id] = 1
            else:
                offer_residency_times[offer_id] += 1

        # Track disappeared offer positions and replaced prices
        for _, row in disappeared_offers.iterrows():
            last_position = row['order_n']
            replacement_offer = curr_scan[curr_scan['order_n'] == last_position]
            if not replacement_offer.empty:
                all_disappeared_offer_positions.append({
                    'offer_id': row['offer_id'],
                    'last_position': last_position,
                    'last_price': row['prices'],
                    'replacement_price': replacement_offer['prices'].values[0]
                })

        # Track new offer prices and previous prices at their positions
        for _, row in new_offers.iterrows():
            new_position = row['order_n']
            prev_offer_at_position = prev_scan[prev_scan['order_n'] == new_position]
            if not prev_offer_at_position.empty:
                all_new_offer_prices.append({
                    'new_offer_id': row['offer_id'],
                    'new_price': row['prices'],
                    'previous_price_at_position': prev_offer_at_position['prices'].values[0]
                })

    # Concatenate results for all scans
    quantity_changes_df = pd.concat(all_quantity_changes)
    disappeared_offers_df = pd.concat(all_disappeared_offers)
    new_offers_df = pd.concat(all_new_offers)

    # Convert list of dicts to DataFrame
    disappeared_offer_positions_df = pd.DataFrame(all_disappeared_offer_positions)
    new_offer_prices_df = pd.DataFrame(all_new_offer_prices)

    # Convert offer_residency_times to DataFrame
    residency_times_df = pd.DataFrame(list(offer_residency_times.items()), columns=['offer_id', 'residency_time'])

    quantity_changes_df.to_csv(f'results/analyzed/{folder_name}_{item_name}_{offer_type}_quantity_changes.csv', index=False)
    disappeared_offers_df.to_csv(f'results/analyzed/{folder_name}_{item_name}_{offer_type}_disappeared_offers.csv', index=False)
    new_offers_df.to_csv(f'results/analyzed/{folder_name}_{item_name}_{offer_type}_new_offers.csv', index=False)
    disappeared_offer_positions_df.to_csv(f'results/analyzed/{folder_name}_{item_name}_{offer_type}_disappeared_offer_positions.csv', index=False)
    new_offer_prices_df.to_csv(f'results/analyzed/{folder_name}_{item_name}_{offer_type}_new_offer_prices.csv', index=False)
    residency_times_df.to_csv(f'results/analyzed/{folder_name}_{item_name}_{offer_type}_residency_times.csv', index=False)
