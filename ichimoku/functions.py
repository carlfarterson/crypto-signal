from datetime import datetime, timedelta

# Function to extend table by the displacement
def extend_df(df, displacement):
    df['date'] = [datetime.strptime(hr, '%Y-%m-%d %H:%M:%S') for hr in df['date']]
    last_date = df['date'].at[len(df)-1]
    dates = [last_date + timedelta(hours=i+1) for i in range(displacement)]
    df = df.append({'date': dates}, ignore_index=True, sort=False)


# Tenkan (conversion line) = (highest high + highest low)/2 for the past 9 periods
# Kijun (base line) = (highest high + lowest low)/2 for the past 26 periods
def make_lines(df, **kwargs):
    for i in kwargs:
        high = df['high'].rolling(window=kwargs[i]).max()
        low = df['low'].rolling(window=kwargs[i]).min()
        df[i] = (high + low)/2


# Chikou (lagging span) = Current closing price time-shifted backwards 26 periods
# Senkou span A (leading span A) = (tenkan + kijun)/2 time-shifted forwards 26 periods
# Senkou span B (leading span B) = (highest high + lowest low)/2 for past 52 periods, shifted forwards 26 periods
def make_spans(df, displacement, senkou_b_period):
    df['chikou'] = df['close'].shift(-displacement)
    df['senkou_a'] = (df['tenkan'] + df['kijun']) / 2

    make_lines(df, senkou_b=senkou_b_period)
    df[['senkou_a', 'senkou_b']] = df[['senkou_a', 'senkou_b']].shift(displacement)
