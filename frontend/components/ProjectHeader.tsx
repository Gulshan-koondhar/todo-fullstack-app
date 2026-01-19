'use client';

import { Button } from '@/components/ui/button';
import { MoreHorizontal } from 'lucide-react';

interface ProjectHeaderProps {
  projectName: string;
}

export function ProjectHeader({ projectName }: ProjectHeaderProps) {
  return (
    <header className="sticky top-0 z-10 bg-background border-b py-4 px-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold">{projectName}</h1>

        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            Share
          </Button>

          <Button variant="outline" size="sm">
            Insights
          </Button>

          <Button variant="outline" size="sm" className="p-2">
            <MoreHorizontal className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </header>
  );
}