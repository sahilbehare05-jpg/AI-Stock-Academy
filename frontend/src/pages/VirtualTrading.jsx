import React, { useEffect, useRef, useState } from 'react'
import {
  createChart,
  CandlestickSeries,
  HistogramSeries,
   LineSeries,
  ColorType,
} from 'lightweight-charts'

import {
  Search,
  RefreshCw,
  Wallet,
  TrendingUp,
  TrendingDown,
  ArrowUpCircle,
  ArrowDownCircle,
  Briefcase,
} from 'lucide-react'
import api from '../services/api'
import { useTranslation } from 'react-i18next'


// ============================================================
// TIMEFRAMES
// ============================================================

const INTRADAY_TIMEFRAMES = [
  { value: '15s', label: '15s' },
  { value: '30s', label: '30s' },
  { value: '1m', label: '1m' },
  { value: '3m', label: '3m' },
  { value: '5m', label: '5m' },
  { value: '10m', label: '10m' },
  { value: '15m', label: '15m' },
  { value: '30m', label: '30m' },
  { value: '1H', label: '1H' },
]

const PERIODS = [
  { value: '1d', label: '1D' },
  { value: '1w', label: '1W' },
  { value: '1mo', label: '1M' },
  { value: '3mo', label: '3M' },
  { value: '6mo', label: '6M' },
  { value: '1y', label: '1Y' },
  { value: '5y', label: '5Y' },
]


// ============================================================
// INTRADAY PERIOD MAPPING
// ============================================================

const PERIOD_FOR_TIMEFRAME = {
  '15s': '1d',
  '30s': '1d',
  '1m': '1d',
  '3m': '1d',
  '5m': '1d',
  '10m': '1d',
  '15m': '1d',
  '30m': '1d',
  '1H': '1mo',
}


// ============================================================
// TRADING CHART
// ============================================================

// ============================================================
// SIMULATED 15s / 30s CANDLES
// Uses 1-minute market data as the base.
// These are virtual/simulated candles, not real exchange data.
// ============================================================

function createSimulatedCandles(history, timeframe) {
  if (!history?.length) return history

  if (!['15s', '30s'].includes(timeframe)) {
    return history
  }

  const secondsPerCandle =
    timeframe === '15s' ? 15 : 30

  const result = []

  history.forEach((item) => {
    const rawDate = item.Date || item.Datetime
    const baseTime =
      Math.floor(new Date(rawDate).getTime() / 1000)

    const open = Number(item.Open)
    const high = Number(item.High)
    const low = Number(item.Low)
    const close = Number(item.Close)
    const volume = Number(item.Volume) || 0

    if (
      !Number.isFinite(baseTime) ||
      !Number.isFinite(open) ||
      !Number.isFinite(high) ||
      !Number.isFinite(low) ||
      !Number.isFinite(close)
    ) {
      return
    }

    const parts = 60 / secondsPerCandle

    for (let i = 0; i < parts; i++) {
      const progress = (i + 1) / parts

      const simulatedOpen =
        i === 0
          ? open
          : open + (close - open) * (i / parts)

      const simulatedClose =
        i === parts - 1
          ? close
          : open + (close - open) * progress

      const range = high - low

      const simulatedHigh =
        Math.max(
          simulatedOpen,
          simulatedClose,
          open + range * progress,
        )

      const simulatedLow =
        Math.min(
          simulatedOpen,
          simulatedClose,
          open - range * progress,
        )

      result.push({
        time:
          baseTime +
          i * secondsPerCandle,

        open: simulatedOpen,
        high: simulatedHigh,
        low: simulatedLow,
        close: simulatedClose,

        volume:
          volume > 0
            ? volume / parts
            : 0,
      })
    }
  })

  return result.sort(
    (a, b) => a.time - b.time,
  )
}
function TradingChart({ history, indicators,timeframe }) {
  const containerRef = useRef(null)

  useEffect(() => {
    if (!containerRef.current || !history?.length) {
      return
    }

    const container = containerRef.current

    const chart = createChart(container, {
      width: container.clientWidth,
      height: 520,

      layout: {
        background: {
          type: ColorType.Solid,
          color: '#07111f',
        },
        textColor: '#94a3b8',
      },

      grid: {
        vertLines: {
          color: 'rgba(255,255,255,0.04)',
        },
        horzLines: {
          color: 'rgba(255,255,255,0.04)',
        },
      },

      crosshair: {
        mode: 1,
      },

      rightPriceScale: {
        borderColor: 'rgba(255,255,255,0.08)',
      },

      timeScale: {
        borderColor: 'rgba(255,255,255,0.08)',
        timeVisible: true,
        secondsVisible: false,
      },
    })

    // =========================================================
    // CANDLESTICKS
    // =========================================================

    const candleSeries = chart.addSeries(
      CandlestickSeries,
      {
        upColor: '#22c55e',
        downColor: '#ef4444',
        borderUpColor: '#22c55e',
        borderDownColor: '#ef4444',
        wickUpColor: '#22c55e',
        wickDownColor: '#ef4444',
      },
    )

    // =========================================================
    // VOLUME
    // =========================================================

    const volumeSeries = chart.addSeries(
      HistogramSeries,
      {
        priceFormat: {
          type: 'volume',
        },
        priceScaleId: '',
      },
    )

    chart.priceScale('').applyOptions({
      scaleMargins: {
        top: 0.78,
        bottom: 0,
      },
    })

    // =========================================================
    // CLEAN HISTORY
    // =========================================================

    const chartHistory = createSimulatedCandles(
  history,
  timeframe,
)

const candles = chartHistory
  .map((item) => {
    const rawDate = item.Date || item.Datetime

    const timestamp = item.time
      ? Number(item.time)
      : Math.floor(
          new Date(rawDate).getTime() / 1000,
        )

    return {
      time: timestamp,
      open: Number(
        item.open ?? item.Open,
      ),
      high: Number(
        item.high ?? item.High,
      ),
      low: Number(
        item.low ?? item.Low,
      ),
      close: Number(
        item.close ?? item.Close,
      ),
    }
  })
      .filter(
        (item) =>
          Number.isFinite(item.time) &&
          Number.isFinite(item.open) &&
          Number.isFinite(item.high) &&
          Number.isFinite(item.low) &&
          Number.isFinite(item.close),
      )
      .sort((a, b) => a.time - b.time)

    // =========================================================
    // SET CANDLES
    // =========================================================

    if (candles.length) {
      candleSeries.setData(candles)
    }

    // =========================================================
    // SET VOLUME
    // =========================================================

    const volumes = chartHistory
      .map((item) => {
        const rawDate = item.Date || item.Datetime

        const timestamp = Math.floor(
          new Date(rawDate).getTime() / 1000,
        )

        const open = Number(item.Open)
        const close = Number(item.Close)

        return {
          time: timestamp,
          value: Number(item.Volume || 0),
          color:
            close >= open
              ? 'rgba(34,197,94,0.35)'
              : 'rgba(239,68,68,0.35)',
        }
      })
      .filter(
        (item) =>
          Number.isFinite(item.time) &&
          Number.isFinite(item.value),
      )
      .sort((a, b) => a.time - b.time)

    if (volumes.length) {
      volumeSeries.setData(volumes)
    }

    // =========================================================
    // INDICATOR HELPER
    // =========================================================

    const createLine = (field, color, title) => {
      if (!indicators[field]) {
        return null
      }

      const series = chart.addSeries(
        LineSeries,
        {
          color,
          lineWidth: 2,
          title,
          priceLineVisible: false,
          lastValueVisible: false,
        },
      )

      const data = history
        .map((item) => {
          const rawDate =
            item.Date || item.Datetime

          const timestamp = Math.floor(
            new Date(rawDate).getTime() / 1000,
          )

          const value = Number(item[field])

          return {
            time: timestamp,
            value,
          }
        })
        .filter(
          (item) =>
            Number.isFinite(item.time) &&
            Number.isFinite(item.value),
        )
        .sort((a, b) => a.time - b.time)

      if (data.length) {
        series.setData(data)
      }

      return series
    }

    // =========================================================
    // MOVING AVERAGES
    // =========================================================

    createLine(
      'SMA_20',
      '#38bdf8',
      'SMA 20',
    )

    createLine(
      'SMA_50',
      '#a78bfa',
      'SMA 50',
    )

    createLine(
      'EMA_20',
      '#f59e0b',
      'EMA 20',
    )

    createLine(
      'EMA_50',
      '#f97316',
      'EMA 50',
    )

    // =========================================================
    // VWAP
    // =========================================================

    createLine(
      'VWAP',
      '#eab308',
      'VWAP',
    )

    // =========================================================
    // BOLLINGER BANDS
    // =========================================================

    createLine(
      'BB_UPPER',
      '#60a5fa',
      'BB Upper',
    )

    createLine(
      'BB_MIDDLE',
      '#94a3b8',
      'BB Middle',
    )

    createLine(
      'BB_LOWER',
      '#60a5fa',
      'BB Lower',
    )
    // =========================================================
// RSI PANEL
// =========================================================

if (indicators.RSI_14) {
  const rsiSeries = chart.addSeries(
    LineSeries,
    {
      pane: 1,
      color: '#a78bfa',
      lineWidth: 2,
      title: 'RSI 14',
      priceLineVisible: false,
      lastValueVisible: true,
    },
  )

  const rsiData = history
    .map((item) => {
      const rawDate =
        item.Date || item.Datetime

      const timestamp = Math.floor(
        new Date(rawDate).getTime() / 1000,
      )

      return {
        time: timestamp,
        value: Number(item.RSI_14),
      }
    })
    .filter(
      (item) =>
        Number.isFinite(item.time) &&
        Number.isFinite(item.value),
    )
    .sort((a, b) => a.time - b.time)

  if (rsiData.length) {
    rsiSeries.setData(rsiData)
  }

  const rsiUpper = chart.addSeries(
    LineSeries,
    {
      pane: 1,
      color: 'rgba(239,68,68,0.45)',
      lineWidth: 1,
      title: 'Overbought 70',
      priceLineVisible: false,
      lastValueVisible: false,
    },
  )

  const rsiLower = chart.addSeries(
    LineSeries,
    {
      pane: 1,
      color: 'rgba(34,197,94,0.45)',
      lineWidth: 1,
      title: 'Oversold 30',
      priceLineVisible: false,
      lastValueVisible: false,
    },
  )

  const rsiLevels = rsiData.map((item) => ({
    time: item.time,
    value: 70,
  }))

  const rsiLowerLevels = rsiData.map((item) => ({
    time: item.time,
    value: 30,
  }))

  if (rsiLevels.length) {
    rsiUpper.setData(rsiLevels)
    rsiLower.setData(rsiLowerLevels)
  }

  if (chart.panes()[1]) {
  chart.panes()[1].setHeight(140)
}
}


// =========================================================
// MACD PANEL
// =========================================================

if (indicators.MACD) {
  const macdSeries = chart.addSeries(
    LineSeries,
    {
      pane: 2,
      color: '#38bdf8',
      lineWidth: 2,
      title: 'MACD',
      priceLineVisible: false,
      lastValueVisible: true,
    },
  )

  const signalSeries = chart.addSeries(
    LineSeries,
    {
      pane: 2,
      color: '#f59e0b',
      lineWidth: 2,
      title: 'Signal',
      priceLineVisible: false,
      lastValueVisible: true,
    },
  )

  const macdData = history
    .map((item) => {
      const rawDate =
        item.Date || item.Datetime

      const timestamp = Math.floor(
        new Date(rawDate).getTime() / 1000,
      )

      return {
        time: timestamp,
        value: Number(item.MACD),
      }
    })
    .filter(
      (item) =>
        Number.isFinite(item.time) &&
        Number.isFinite(item.value),
    )
    .sort((a, b) => a.time - b.time)

  const signalData = history
    .map((item) => {
      const rawDate =
        item.Date || item.Datetime

      const timestamp = Math.floor(
        new Date(rawDate).getTime() / 1000,
      )

      return {
        time: timestamp,
        value: Number(item.MACD_SIGNAL),
      }
    })
    .filter(
      (item) =>
        Number.isFinite(item.time) &&
        Number.isFinite(item.value),
    )
    .sort((a, b) => a.time - b.time)

  if (macdData.length) {
    macdSeries.setData(macdData)
  }

  if (signalData.length) {
    signalSeries.setData(signalData)
  }

  if (chart.panes()[2]) {
  chart.panes()[2].setHeight(140)
}
}
// =========================================================
// STOCHASTIC PANEL
// =========================================================

if (indicators.STOCHASTIC) {
  const stochasticK = chart.addSeries(
    LineSeries,
    {
      pane: 3,
      color: '#38bdf8',
      lineWidth: 2,
      title: 'Stoch K',
      priceLineVisible: false,
      lastValueVisible: true,
    },
  )

  const stochasticD = chart.addSeries(
    LineSeries,
    {
      pane: 3,
      color: '#f59e0b',
      lineWidth: 2,
      title: 'Stoch D',
      priceLineVisible: false,
      lastValueVisible: true,
    },
  )

  const kData = history
    .map((item) => {
      const rawDate = item.Date || item.Datetime

      return {
        time: Math.floor(
          new Date(rawDate).getTime() / 1000,
        ),
        value: Number(item.STOCH_K),
      }
    })
    .filter(
      (item) =>
        Number.isFinite(item.time) &&
        Number.isFinite(item.value),
    )
    .sort((a, b) => a.time - b.time)

  const dData = history
    .map((item) => {
      const rawDate = item.Date || item.Datetime

      return {
        time: Math.floor(
          new Date(rawDate).getTime() / 1000,
        ),
        value: Number(item.STOCH_D),
      }
    })
    .filter(
      (item) =>
        Number.isFinite(item.time) &&
        Number.isFinite(item.value),
    )
    .sort((a, b) => a.time - b.time)

  if (kData.length) {
    stochasticK.setData(kData)
  }

  if (dData.length) {
    stochasticD.setData(dData)
  }

  if (chart.panes()[3]) {
  chart.panes()[3].setHeight(140)
}
}


// =========================================================
// ATR PANEL
// =========================================================

if (indicators.ATR_14) {
  const atrSeries = chart.addSeries(
    LineSeries,
    {
      pane: 4,
      color: '#a78bfa',
      lineWidth: 2,
      title: 'ATR 14',
      priceLineVisible: false,
      lastValueVisible: true,
    },
  )

  const atrData = history
    .map((item) => {
      const rawDate = item.Date || item.Datetime

      return {
        time: Math.floor(
          new Date(rawDate).getTime() / 1000,
        ),
        value: Number(item.ATR_14),
      }
    })
    .filter(
      (item) =>
        Number.isFinite(item.time) &&
        Number.isFinite(item.value),
    )
    .sort((a, b) => a.time - b.time)

  if (atrData.length) {
    atrSeries.setData(atrData)
  }

  if (chart.panes()[4]) {
  chart.panes()[4].setHeight(130)
}
}


// =========================================================
// CCI PANEL
// =========================================================

if (indicators.CCI_20) {
  const cciSeries = chart.addSeries(
    LineSeries,
    {
      pane: 5,
      color: '#f97316',
      lineWidth: 2,
      title: 'CCI 20',
      priceLineVisible: false,
      lastValueVisible: true,
    },
  )

  const cciData = history
    .map((item) => {
      const rawDate = item.Date || item.Datetime

      return {
        time: Math.floor(
          new Date(rawDate).getTime() / 1000,
        ),
        value: Number(item.CCI_20),
      }
    })
    .filter(
      (item) =>
        Number.isFinite(item.time) &&
        Number.isFinite(item.value),
    )
    .sort((a, b) => a.time - b.time)

  if (cciData.length) {
    cciSeries.setData(cciData)
  }

  if (chart.panes()[5]) {
  chart.panes()[5].setHeight(130)
}
}


// =========================================================
// OBV PANEL
// =========================================================

if (indicators.OBV) {
  const obvSeries = chart.addSeries(
    LineSeries,
    {
      pane: 6,
      color: '#22c55e',
      lineWidth: 2,
      title: 'OBV',
      priceLineVisible: false,
      lastValueVisible: true,
    },
  )

  const obvData = history
    .map((item) => {
      const rawDate = item.Date || item.Datetime

      return {
        time: Math.floor(
          new Date(rawDate).getTime() / 1000,
        ),
        value: Number(item.OBV),
      }
    })
    .filter(
      (item) =>
        Number.isFinite(item.time) &&
        Number.isFinite(item.value),
    )
    .sort((a, b) => a.time - b.time)

  if (obvData.length) {
    obvSeries.setData(obvData)
  }

  if (chart.panes()[6]) {
  chart.panes()[6].setHeight(130)
}
}

    chart.timeScale().fitContent()

    // =========================================================
    // RESPONSIVE
    // =========================================================

    const resizeObserver = new ResizeObserver(() => {
      if (!containerRef.current) {
        return
      }

      chart.applyOptions({
        width: containerRef.current.clientWidth,
      })
    })

    resizeObserver.observe(container)

    // =========================================================
    // CLEANUP
    // =========================================================

    return () => {
      resizeObserver.disconnect()
      chart.remove()
    }
  }, [history, indicators ,timeframe])

  return (
    <div
      ref={containerRef}
      className="w-full min-h-[520px]"
    />
  )
}


// ============================================================
// MAIN COMPONENT
// ============================================================

export default function VirtualTrading() {
    const { t, i18n } = useTranslation()

  // ----------------------------------------------------------
  // STOCK
  // ----------------------------------------------------------

  const [symbol, setSymbol] =
    useState('AAPL')

  const [searchInput, setSearchInput] =
    useState('AAPL')


  // ----------------------------------------------------------
  // TIMEFRAME
  // ----------------------------------------------------------

  const [timeframe, setTimeframe] =
    useState('5m')

  const [period, setPeriod] =
    useState('1d')


  // ----------------------------------------------------------
  // DATA
  // ----------------------------------------------------------

  const [stock, setStock] =
    useState(null)

  const [wallet, setWallet] =
    useState(null)

  const [portfolio, setPortfolio] =
    useState(null)


  // ----------------------------------------------------------
  // LIVE PRICE
  // ----------------------------------------------------------

  const [livePrice, setLivePrice] =
    useState(null)

  const [liveLoading, setLiveLoading] =
    useState(false)

  const [lastLiveUpdate, setLastLiveUpdate] =
    useState(null)


  // ----------------------------------------------------------
  // ORDER
  // ----------------------------------------------------------

  const [quantity, setQuantity] =
    useState(1)
   const [indicators, setIndicators] = useState({
  SMA_20: true,
  SMA_50: false,
  EMA_20: true,
  EMA_50: false,

  VWAP: false,

  BB_UPPER: false,
  BB_MIDDLE: false,
  BB_LOWER: false,

  RSI_14: false,
  MACD: false,

  STOCHASTIC: false,
  ATR_14: false,
  CCI_20: false,
  OBV: false,
})
const toggleIndicator = (indicator) => {
  setIndicators((previous) => ({
    ...previous,
    [indicator]: !previous[indicator],
  }))
}


  // ----------------------------------------------------------
  // UI
  // ----------------------------------------------------------

  const [loading, setLoading] =
    useState(true)

  const [trading, setTrading] =
    useState(false)

  const [error, setError] =
    useState('')

  const [message, setMessage] =
    useState('')


  // ==========================================================
  // LOAD STOCK + WALLET + PORTFOLIO
  // ==========================================================

  const loadData = async (
    selectedSymbol = symbol,
    selectedPeriod = period,
    selectedTimeframe = timeframe,
  ) => {

    try {

      setLoading(true)
      setError('')


      const [
        stockResponse,
        walletResponse,
        portfolioResponse,
      ] = await Promise.all([

        api.get(
  `/api/stocks/${encodeURIComponent(
    selectedSymbol,
  )}?period=${selectedPeriod}&interval=${
    ['15s', '30s'].includes(selectedTimeframe)
      ? '1m'
      : selectedTimeframe
  }`,
),

        api.get(
          '/api/wallet',
        ),

        api.get(
          '/api/portfolio',
        ),

      ])


      setStock(
        stockResponse.data.data,
      )

      setWallet(
        walletResponse.data.data,
      )

      setPortfolio(
        portfolioResponse.data.data,
      )

    } catch (err) {

      setError(
  err.response?.data?.detail ||
  t('virtualTrading.tradingLoadError'),
)

    } finally {

      setLoading(false)

    }
  }


  // ==========================================================
  // FETCH LIVE PRICE
  // ==========================================================

  const fetchLivePrice = async () => {

    if (!symbol) {
      return
    }


    try {

      setLiveLoading(true)


      const response = await api.get(
        `/api/stocks/${encodeURIComponent(
          symbol,
        )}/live`,
      )


      const data =
        response.data.data


      setLivePrice(data)

      setLastLiveUpdate(
        new Date(),
      )

    } catch (err) {

      console.error(
        'Live price update failed:',
        err,
      )

    } finally {

      setLiveLoading(false)

    }
  }


  // ==========================================================
  // INITIAL LOAD
  // ==========================================================

  useEffect(() => {

    loadData()

  }, [])


  // ==========================================================
  // LIVE PRICE AUTO REFRESH
  // EVERY 15 SECONDS
  // ==========================================================

  useEffect(() => {

    if (!symbol) {
      return
    }


    fetchLivePrice()


    const intervalId =
      setInterval(() => {

        fetchLivePrice()

      }, 15000)


    return () => {

      clearInterval(intervalId)

    }

  }, [symbol])


  // ==========================================================
  // CURRENT DATA
  // ==========================================================

  const latest =
    stock?.latest || {}

  const history =
    stock?.history || []


  // ==========================================================
  // CURRENT PRICE
  // LIVE PRICE HAS PRIORITY
  // ==========================================================

  const currentPrice =
    Number(
      livePrice?.price ||
        latest.close ||
        0,
    )


  // ==========================================================
  // PREVIOUS CLOSE
  // ==========================================================

  const previousClose =
    Number(
      livePrice?.previous_close ||
        currentPrice,
    )


  // ==========================================================
  // PRICE CHANGE
  // ==========================================================

  const change =
    Number(
      livePrice?.change ??
        (
          currentPrice -
          previousClose
        ),
    )


  // ==========================================================
  // CHANGE %
  // ==========================================================

  const changePercent =
    Number(
      livePrice?.change_percent ??
        (
          previousClose > 0
            ? (
                change /
                previousClose
              ) * 100
            : 0
        ),
    )


  // ==========================================================
  // ORDER VALUE
  // ==========================================================

  const orderValue =
    currentPrice *
    Number(quantity || 0)


  // ==========================================================
  // TIMEFRAME CHANGE
  // ==========================================================

  const handleTimeframe = async (
    newTimeframe,
  ) => {

    setTimeframe(
      newTimeframe,
    )


    const newPeriod =
      PERIOD_FOR_TIMEFRAME[
        newTimeframe
      ] || '1d'


    setPeriod(
      newPeriod,
    )


    await loadData(
      symbol,
      newPeriod,
      newTimeframe,
    )


    // Immediately update live price
    await fetchLivePrice()
  }


  // ==========================================================
  // PERIOD CHANGE
  // ==========================================================

  const handlePeriod = async (
    newPeriod,
  ) => {

    setPeriod(
      newPeriod,
    )


    let selectedTimeframe =
      timeframe


    // Long-term chart
    // uses daily candles.

    if (
      ['1y', '5y'].includes(
        newPeriod,
      )
    ) {

      selectedTimeframe =
        '1D'

      setTimeframe(
        '1D',
      )
    }


    await loadData(
      symbol,
      newPeriod,
      selectedTimeframe,
    )


    await fetchLivePrice()
  }


  // ==========================================================
  // SEARCH STOCK
  // ==========================================================

  const searchStock = async (
    event,
  ) => {

    event.preventDefault()


    const cleanSymbol =
      searchInput
        .trim()
        .toUpperCase()


    if (!cleanSymbol) {
      return
    }


    setSymbol(
      cleanSymbol,
    )

    setMessage('')


    await loadData(
      cleanSymbol,
      period,
      timeframe,
    )
  }


  // ==========================================================
  // BUY / SELL
  // ==========================================================

  const trade = async (
  type,
  tradeQuantity = quantity,
  tradeSymbol = symbol,
  tradePrice = currentPrice,
) => {

    if (!tradePrice) {

      setError(
  t('virtualTrading.currentPriceUnavailable'),
)

      return
    }


    if (
      Number(tradeQuantity) <= 0
    ) {

      setError(
  t('virtualTrading.quantityGreaterZero'),
)

      return
    }


    try {

      setTrading(true)

      setError('')

      setMessage('')


      const endpoint =
        type === 'BUY'
          ? '/api/trading/buy'
          : '/api/trading/sell'


      const response =
        await api.post(
          endpoint,
          {
            symbol:
              tradeSymbol.toUpperCase(),

            quantity:
              Number(tradeQuantity),

            price:
              tradePrice,
          },
        )


      setMessage(
        response.data.data.message,
      )


      await loadData(
        symbol,
        period,
        timeframe,
      )


      await fetchLivePrice()

    } catch (err) {

      setError(
        err.response?.data?.detail ||
          `${type} ${t('virtualTrading.orderFailed')}`,
      )

    } finally {

      setTrading(false)

    }
  }


  // ==========================================================
  // UI
  // ==========================================================

  return (

    <div className="space-y-5 pb-10">


      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">

        <div>

          <h1 className="text-2xl font-bold text-white">
          {t('virtualTrading.title')}
          </h1>

          <p className="text-sm text-slate-400 mt-1">
           {t('virtualTrading.subtitle')}
          </p>

        </div>


        <button
          onClick={() =>
            loadData(
              symbol,
              period,
              timeframe,
            )
          }
          disabled={loading}
          className="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl border border-white/10 text-slate-300 hover:text-white hover:bg-white/5"
        >

          <RefreshCw
            size={16}
            className={
              loading
                ? 'animate-spin'
                : ''
            }
          />

          R{t('virtualTrading.refresh')}

        </button>

      </div>


      {/* =====================================================
          ERROR
      ===================================================== */}

      {error && (

        <div className="rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">

          {error}

        </div>

      )}


      {/* =====================================================
          SUCCESS
      ===================================================== */}

      {message && (

        <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-400">

          {message}

        </div>

      )}


      {/* =====================================================
          SEARCH
      ===================================================== */}

      <div className="card p-4">

        <form
          onSubmit={searchStock}
          className="flex flex-col sm:flex-row gap-3"
        >

          <div className="relative flex-1">

            <Search
              size={18}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
            />

            <input
              value={searchInput}
              onChange={(event) =>
                setSearchInput(
                  event.target.value.toUpperCase(),
                )
              }
              placeholder={t('virtualTrading.searchPlaceholder')}
              className="input-field pl-10 uppercase"
            />

          </div>


          <button
            type="submit"
            className="btn-primary px-6"
          >

            <Search size={17} />

            {t('virtualTrading.search')}

          </button>

        </form>

      </div>


      {/* =====================================================
          STOCK CHART
      ===================================================== */}

      <div className="card overflow-hidden">


        {/* STOCK HEADER */}

        <div className="px-5 py-4 border-b border-white/5">

          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">


            <div>

              <div className="flex items-center gap-3">

                <h2 className="text-2xl font-bold text-white">
                  {symbol}
                </h2>


                {/* LIVE BADGE */}

                <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center gap-1.5">

                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />

                  {t('virtualTrading.live')}

                </span>

              </div>


              <p className="text-xs text-slate-500 mt-1">
                {t('virtualTrading.chartDescription')}
              </p>

            </div>


            {/* PRICE */}

            <div className="text-left md:text-right">

              <div className="text-3xl font-bold text-white">

                ₹{currentPrice.toFixed(2)}

              </div>


              <div
                className={`flex items-center md:justify-end gap-1 text-sm ${
                  change >= 0
                    ? 'text-emerald-400'
                    : 'text-red-400'
                }`}
              >

                {change >= 0 ? (
                  <TrendingUp size={15} />
                ) : (
                  <TrendingDown size={15} />
                )}


                {change >= 0 ? '+' : ''}

                ₹{change.toFixed(2)}

                {' '}

                (
                {changePercent >= 0
                  ? '+'
                  : ''}

                {changePercent.toFixed(2)}

                %)

              </div>


              {/* LAST UPDATE */}

              {lastLiveUpdate && (

                <div className="text-[10px] text-slate-500 mt-1">

                  {t('virtualTrading.updated')}{' '}

                  {lastLiveUpdate.toLocaleTimeString()}

                  {liveLoading &&
                    ' • Updating...'}

                </div>

              )}

            </div>

          </div>

        </div>


        {/* ===================================================
            INTRADAY
        =================================================== */}

        <div className="px-5 pt-4">

          <p className="text-xs uppercase tracking-wider text-slate-500 mb-2">
           {t('virtualTrading.intraday')}
          </p>


          <div className="flex flex-wrap gap-1.5">

            {INTRADAY_TIMEFRAMES.map(
              ({
                value,
                label,
              }) => (

                <button
                  key={value}
                  onClick={() =>
                    handleTimeframe(
                      value,
                    )
                  }
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium ${
                    timeframe === value
                      ? 'bg-accent-blue/15 text-accent-blue border border-accent-blue/25'
                      : 'text-slate-500 hover:text-white hover:bg-white/5'
                  }`}
                >

                  {label}

                </button>

              ),
            )}

          </div>

        </div>


        {/* ===================================================
            PERIOD
        =================================================== */}

        <div className="px-5 pt-4">

          <p className="text-xs uppercase tracking-wider text-slate-500 mb-2">
           {t('virtualTrading.period')}
          </p>


          <div className="flex flex-wrap gap-1.5">

            {PERIODS.map(
              ({
                value,
                label,
              }) => (

                <button
                  key={value}
                  onClick={() =>
                    handlePeriod(
                      value,
                    )
                  }
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium ${
                    period === value
                      ? 'bg-accent-blue/15 text-accent-blue border border-accent-blue/25'
                      : 'text-slate-500 hover:text-white hover:bg-white/5'
                  }`}
                >

                  {label}

                </button>

              ),
            )}

          </div>

        </div>


       {/* =====================================================
    INDICATORS
===================================================== */}

<div className="px-5 pt-4">

  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">

    <div>
      <p className="text-xs uppercase tracking-wider text-slate-500">
        {t('virtualTrading.technicalIndicators')}
      </p>

      <p className="text-xs text-slate-500 mt-1">
        {t('virtualTrading.selectIndicators')}
      </p>
    </div>

    <div className="flex flex-wrap gap-2">

      {[
        { key: 'SMA_20', label: 'SMA 20' },
        { key: 'SMA_50', label: 'SMA 50' },
        { key: 'EMA_20', label: 'EMA 20' },
        { key: 'EMA_50', label: 'EMA 50' },
        { key: 'VWAP', label: 'VWAP' },
        { key: 'BB_UPPER', label: 'Bollinger Bands' },
        { key: 'RSI_14', label: 'RSI 14' },
        { key: 'MACD', label: 'MACD' },
        { key: 'STOCHASTIC', label: 'Stochastic' },
        { key: 'ATR_14', label: 'ATR 14' },
        { key: 'CCI_20', label: 'CCI 20' },
        { key: 'OBV', label: 'OBV' },
      ].map(({ key, label }) => {

        const active =
          key === 'BB_UPPER'
            ? indicators.BB_UPPER
            : indicators[key]

        return (
          <button
            key={key}
            type="button"
            onClick={() => {
              if (key === 'BB_UPPER') {
                const next = !indicators.BB_UPPER

                setIndicators((previous) => ({
                  ...previous,
                  BB_UPPER: next,
                  BB_MIDDLE: next,
                  BB_LOWER: next,
                }))
              } else {
                toggleIndicator(key)
              }
            }}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition ${
              active
                ? 'bg-accent-blue/15 text-accent-blue border-accent-blue/30'
                : 'bg-white/[0.02] text-slate-400 border-white/10 hover:text-white hover:bg-white/5'
            }`}
          >
            {active ? '✓ ' : ''}
            {label}
          </button>
        )
      })}

    </div>

  </div>

</div>
 {/* CHART */}

        <div className="px-3 pb-3 pt-2">

          <TradingChart
  history={history}
  indicators={indicators}
  timeframe={timeframe}
/>

        </div>


        {/* MARKET DATA */}

        <div className="grid grid-cols-2 md:grid-cols-5 border-t border-white/5">

          <MarketStat
            label={t('virtualTrading.open')}
            value={latest.open}
          />

          <MarketStat
            label={t('virtualTrading.high')}
            value={latest.high}
          />

          <MarketStat
            label={t('virtualTrading.low')}
            value={latest.low}
          />

          <MarketStat
            label={t('virtualTrading.volume')}
            value={latest.volume}
            volume
          />

          <MarketStat
            label={t('virtualTrading.rsi')}
            value={latest.rsi_14}
          />

        </div>

      </div>


      {/* =====================================================
          ORDER + WALLET
      ===================================================== */}

      <div className="grid xl:grid-cols-3 gap-5">


        {/* ORDER */}

        <div className="xl:col-span-2 card p-5">

          <h2 className="font-semibold text-white mb-5">
           {t('virtualTrading.placeOrder')}
          </h2>


          <div className="grid md:grid-cols-3 gap-4">


            {/* STOCK */}

            <div>

              <label className="text-xs text-slate-400 block mb-2">
                {t('virtualTrading.stock')}
              </label>


              <div className="input-field flex items-center text-white font-semibold">

                {symbol}

              </div>

            </div>


            {/* QUANTITY */}

            <div>

              <label className="text-xs text-slate-400 block mb-2">
               {t('virtualTrading.quantity')}
              </label>


              <input
                type="number"
                min="1"
                step="1"
                value={quantity}
                onChange={(event) =>
                  setQuantity(
                    event.target.value,
                  )
                }
                className="input-field"
              />

            </div>


            {/* MARKET PRICE */}

            <div>

              <label className="text-xs text-slate-400 block mb-2">
                {t('virtualTrading.liveMarketPrice')}
              </label>


              <div className="input-field flex items-center text-white font-semibold">

                ₹{currentPrice.toFixed(2)}

              </div>

            </div>

          </div>


          {/* ORDER VALUE */}

          <div className="mt-5 p-4 rounded-xl bg-white/[0.025] border border-white/5 flex items-center justify-between">

            <span className="text-sm text-slate-400">
              {t('virtualTrading.estimatedOrderValue')}
            </span>


            <span className="text-lg font-bold text-white">

              ₹{orderValue.toFixed(2)}

            </span>

          </div>


          {/* BUY SELL */}

          <div className="grid sm:grid-cols-2 gap-3 mt-5">


            <button
              onClick={() =>
                trade('BUY')
              }
              disabled={
                trading ||
                loading ||
                !currentPrice
              }
              className="py-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 font-semibold flex items-center justify-center gap-2 hover:bg-emerald-500/15 disabled:opacity-50"
            >

              <ArrowUpCircle size={19} />

              {trading
                ? t('virtualTrading.processing')
                : 'BUY'}

            </button>


            <button
              onClick={() =>
                trade('SELL')
              }
              disabled={
                trading ||
                loading ||
                !currentPrice
              }
              className="py-3.5 rounded-xl bg-red-500/10 border border-red-500/25 text-red-400 font-semibold flex items-center justify-center gap-2 hover:bg-red-500/15 disabled:opacity-50"
            >

              <ArrowDownCircle size={19} />

              {trading
                ? t('virtualTrading.processing')
                : 'SELL'}

            </button>

          </div>

        </div>


        {/* WALLET */}

        <div className="card p-5">


          <div className="flex items-center gap-3 mb-5">

            <div className="w-10 h-10 rounded-xl bg-accent-blue/10 text-accent-blue flex items-center justify-center">

              <Wallet size={19} />

            </div>


            <div>

              <p className="text-xs text-slate-400">
                {t('virtualTrading.virtualBalance')}
              </p>


              <p className="text-xl font-bold text-white">

                ₹
                {Number(
                  wallet?.balance || 0,
                ).toLocaleString(
                  'en-IN',
                  {
                    minimumFractionDigits: 2,
                  },
                )}

              </p>

            </div>

          </div>


          <div className="space-y-4">


            <InfoRow
              label={t('virtualTrading.portfolioValue')}
              value={`₹${Number(
                portfolio?.total_value || 0,
              ).toFixed(2)}`}
            />


            <InfoRow
             label={t('virtualTrading.totalPnl')}
              value={`${
                Number(
                  portfolio?.total_pnl || 0,
                ) >= 0
                  ? '+'
                  : ''
              }₹${Number(
                portfolio?.total_pnl || 0,
              ).toFixed(2)}`}
              positive={
                Number(
                  portfolio?.total_pnl || 0,
                ) >= 0
              }
            />

          </div>

        </div>

      </div>

 {/* =====================================================
          HOLDINGS
      ===================================================== */}

      <div className="card p-5">

        <div className="flex items-center gap-3 mb-5">

          <Briefcase
            size={19}
            className="text-accent-blue"
          />

          <div>

            <h2 className="font-semibold text-white">
              {t('virtualTrading.myHoldings')}
            </h2>

            <p className="text-xs text-slate-500">
              {t('virtualTrading.currentPositions')}
            </p>

          </div>

        </div>


        {!portfolio?.holdings?.length ? (

          <div className="text-center py-10 text-slate-500 text-sm">

            {t('virtualTrading.noHoldings')}
            {t('virtualTrading.buyToSee')}

          </div>

        ) : (

          <div className="space-y-3">

            {portfolio.holdings.map(
              (holding) => {

                const pnl =
                  Number(holding.pnl || 0)

                const pnlPercent =
                  Number(
                    holding.pnl_percent || 0
                  )

                return (

                  <div
                    key={holding.symbol}
                    className="rounded-xl border border-white/5 p-4"
                  >

                    <div className="grid grid-cols-2 md:grid-cols-7 gap-4">

                      <Value
                        label={t('virtualTrading.symbol')}
                        value={holding.symbol}
                      />

                      <Value
                        label="Quantity"
                        value={holding.quantity}
                      />

                      <Value
                        label={t('virtualTrading.averagePrice')}
                        value={`₹${Number(
                          holding.average_price
                        ).toFixed(2)}`}
                      />

                      <Value
                        label={t('virtualTrading.currentPrice')}
                        value={`₹${Number(
                          holding.current_price
                        ).toFixed(2)}`}
                      />

                      <Value
                        label={t('virtualTrading.marketValue')}
                        value={`₹${Number(
                          holding.market_value
                        ).toFixed(2)}`}
                      />

                      <Value
                        label={t('virtualTrading.pnl')}
                        value={`${
                          pnl >= 0 ? '+' : ''
                        }₹${pnl.toFixed(2)}`}
                        positive={pnl >= 0}
                      />

                      <Value
                        label={t('virtualTrading.pnlPercent')}
                        value={`${
                          pnlPercent >= 0 ? '+' : ''
                        }${pnlPercent.toFixed(2)}%`}
                        positive={pnlPercent >= 0}
                      />

                    </div>


                    {/* EXIT */}

                    <div className="mt-4 pt-4 border-t border-white/5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">

                      <div>

                        <p className="text-xs text-slate-500">
                          Position
                        </p>

                        <p className="text-sm text-slate-300">
                          {holding.quantity} {t('virtualTrading.sharesOpen')}
                        </p>

                      </div>


                      <button
                        type="button"
                        disabled={
                          trading ||
                          loading ||
                          !holding.current_price
                        }
                        onClick={() => {
                          const confirmed =
                            window.confirm(
                            t('virtualTrading.exitConfirm', {
                            quantity: holding.quantity,
    symbol: holding.symbol,
  })
)

                          if (!confirmed) {
                            return
                          }

                          trade(
                            'SELL',
                            Number(holding.quantity),
                            holding.symbol,
                            Number(holding.current_price)
                          )
                        }}
                        className="px-5 py-2.5 rounded-xl bg-red-500/10 border border-red-500/25 text-red-400 font-semibold hover:bg-red-500/15 disabled:opacity-50"
                      >

                        {trading
                        ? t('virtualTrading.exiting')
                        : `${t('virtualTrading.exitAll')} ${holding.symbol}`
                        }

                      </button>

                    </div>

                  </div>

                )
              }
            )}

          </div>

        )}

            </div>

    </div>
  )
}

// ============================================================
// MARKET STAT
// ============================================================

function MarketStat({
  label,
  value,
  volume,
}) {

  if (
    value === null ||
    value === undefined
  ) {

    return (

      <div className="p-4 border-r border-white/5">

        <p className="text-xs text-slate-500">
          {label}
        </p>

        <p className="text-sm text-slate-600 mt-1">
          —
        </p>

      </div>

    )
  }


  const displayValue =
    volume
      ? Number(
          value,
        ).toLocaleString('en-IN')
      : Number(
          value,
        ).toFixed(2)


  return (

    <div className="p-4 border-r border-white/5">

      <p className="text-xs text-slate-500">
        {label}
      </p>

      <p className="text-sm font-semibold text-white mt-1">
        {displayValue}
      </p>

    </div>

  )
}


// ============================================================
// INFO ROW
// ============================================================

function InfoRow({
  label,
  value,
  positive,
}) {

  return (

    <div className="flex items-center justify-between border-b border-white/5 pb-3">

      <span className="text-sm text-slate-400">
        {label}
      </span>


      <span
        className={`text-sm font-semibold ${
          positive === undefined
            ? 'text-white'
            : positive
              ? 'text-emerald-400'
              : 'text-red-400'
        }`}
      >

        {value}

      </span>

    </div>

  )
}


// ============================================================
// HOLDING VALUE
// ============================================================

function Value({
  label,
  value,
  positive,
}) {

  return (

    <div>

      <p className="text-xs text-slate-500">
        {label}
      </p>


      <p
        className={`text-sm font-semibold mt-1 ${
          positive === undefined
            ? 'text-white'
            : positive
              ? 'text-emerald-400'
              : 'text-red-400'
        }`}
      >

        {value}

      </p>

    </div>

  )
}