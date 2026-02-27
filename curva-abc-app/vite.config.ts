import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { readFileSync, writeFileSync, existsSync } from 'fs'
import { resolve } from 'path'
import type { Plugin } from 'vite'

const EXCEL_PATH = 'D:\\Users\\Claudio\\OneDrive\\Nova pasta\\Bd_curva abc\\curva abc.xlsx'
const JSON_PATH = resolve(__dirname, 'public', 'dados.json')

function lerExcelPlugin(): Plugin {
  return {
    name: 'ler-excel',
    configureServer(server) {
      server.middlewares.use('/api/atualizar', async (_req, res) => {
        try {
          if (!existsSync(EXCEL_PATH)) {
            res.writeHead(404, { 'Content-Type': 'application/json' })
            res.end(JSON.stringify({ erro: 'Planilha não encontrada: ' + EXCEL_PATH }))
            return
          }

          const XLSX = await import('xlsx')
          const wb = XLSX.readFile(EXCEL_PATH)
          const ws = wb.Sheets['Produtos mais vendidos']
          if (!ws) {
            res.writeHead(400, { 'Content-Type': 'application/json' })
            res.end(JSON.stringify({ erro: 'Aba "Produtos mais vendidos" não encontrada' }))
            return
          }

          const rows: Record<string, unknown>[] = XLSX.utils.sheet_to_json(ws)

          const normalizar = (s: string) =>
            String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim()

          const parseNum = (v: unknown): number => {
            if (typeof v === 'number') return v
            const s = String(v).replace(/\./g, '').replace(',', '.')
            return parseFloat(s) || 0
          }

          const dados = rows
            .map(row => {
              const keys = Object.keys(row)
              const get = (palavras: string[]) => {
                const k = keys.find(k => palavras.some(p => normalizar(k).includes(p)))
                return k ? row[k] : undefined
              }

              const codigo      = String(get(['cod']) ?? '').trim()
              const descricao   = String(get(['desc', 'prod', 'nome']) ?? '').trim()
              const quantidade  = parseNum(get(['quant', 'qtd', 'qty']))
              const valorUnit   = parseNum(get(['unit', 'unitario', 'preco']))
              const valorTotal  = parseNum(get(['valor', 'total', 'vl']))
              const valorUnitario = valorUnit || (quantidade > 0 ? valorTotal / quantidade : 0)

              return { codigo, descricao, quantidade, valorUnitario }
            })
            .filter(p => p.descricao && (p.quantidade > 0 || p.valorUnitario > 0))

          writeFileSync(JSON_PATH, JSON.stringify(dados, null, 2), 'utf-8')

          res.writeHead(200, { 'Content-Type': 'application/json' })
          res.end(JSON.stringify({ ok: true, total: dados.length }))
        } catch (err) {
          res.writeHead(500, { 'Content-Type': 'application/json' })
          res.end(JSON.stringify({ erro: String(err) }))
        }
      })
    },
  }
}

export default defineConfig({
  plugins: [react(), lerExcelPlugin()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-react': ['react', 'react-dom'],
          'vendor-charts': ['recharts'],
          'vendor-excel': ['xlsx'],
          'vendor-pdf': ['jspdf', 'jspdf-autotable', 'html2canvas'],
        },
      },
    },
    chunkSizeWarningLimit: 1000,
  },
})
